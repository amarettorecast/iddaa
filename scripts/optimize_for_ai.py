import json
import math
import sys
from pathlib import Path
from statistics import mean, stdev


def extract_numeric_odds(bookmaker_entry: dict) -> dict[str, float]:
    """Büro verisinden sayısal oran anahtarlarını ayıklar."""
    skip_keys = {
        "bookmaker_name", "bookmaker", "period", "market",
        "line", "handicap", "is_blocked", "timestamp", "url"
    }
    odds = {}
    for k, v in bookmaker_entry.items():
        if k in skip_keys or v is None:
            continue
        try:
            val = float(v)
            if val > 1.0:
                odds[k] = val
        except (ValueError, TypeError):
            continue
    return odds


def summarize_market(entries: list[dict]) -> dict | None:
    """Büro listesini AI için istatistiksel özete ve adil olasılıklara dönüştürür."""
    if not entries or not isinstance(entries, list):
        return None

    outcome_buckets: dict[str, list[tuple[float, str]]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("is_blocked"):
            continue
        bookie = entry.get("bookmaker_name") or entry.get("bookmaker") or "Unknown"
        odds_map = extract_numeric_odds(entry)
        for outcome, odd_val in odds_map.items():
            outcome_buckets.setdefault(outcome, []).append((odd_val, bookie))

    if not outcome_buckets:
        return None

    summary = {"bookmaker_count": max(len(v) for v in outcome_buckets.values()), "outcomes": {}}
    raw_implied_sum = 0.0

    for outcome, pairs in outcome_buckets.items():
        values = [p[0] for p in pairs]
        avg_odd = round(mean(values), 3)
        max_odd, best_bookie = max(pairs, key=lambda x: x[0])
        spread_sd = round(stdev(values), 3) if len(values) > 1 else 0.0
        raw_prob = 1.0 / avg_odd
        raw_implied_sum += raw_prob

        summary["outcomes"][outcome] = {
            "avg_odd": avg_odd,
            "max_odd": max_odd,
            "best_bookie": best_bookie,
            "std_dev": spread_sd,
            "_raw_prob": raw_prob,
        }

    # Vig (Kar Marjı) temizliği ve Adil Olasılık (No-Vig Fair Probability) hesabı
    if raw_implied_sum > 0:
        summary["market_margin_pct"] = round((raw_implied_sum - 1.0) * 100, 2)
        for out_data in summary["outcomes"].values():
            fair_prob = (out_data.pop("_raw_prob") / raw_implied_sum) * 100
            out_data["fair_prob_pct"] = round(fair_prob, 2)

    # İki ihtimalli marketlerde dengelilik skoru (Ana barem tespiti için)
    if len(summary["outcomes"]) == 2:
        probs = [d["fair_prob_pct"] for d in summary["outcomes"].values()]
        summary["balance_diff"] = round(abs(probs[0] - probs[1]), 2)

    return summary


def optimize_match(match: dict) -> dict:
    """Tek bir NBA maçının tüm marketlerini AI için yapılandırır."""
    meta_keys = {
        "sport", "country", "league", "home_team", "away_team",
        "match_date", "kickoff", "match_url", "venue", "scraped_at_utc"
    }
    clean_match = {k: match.get(k) for k in meta_keys if match.get(k) is not None}

    core_markets = {}
    over_under_lines = {}
    handicap_lines = {}

    for key, val in match.items():
        if key in meta_keys or not isinstance(val, list):
            continue
        market_clean = key.removesuffix("_market")
        summarized = summarize_market(val)
        if not summarized:
            continue

        if market_clean.startswith("over_under"):
            over_under_lines[market_clean] = summarized
        elif "handicap" in market_clean:
            handicap_lines[market_clean] = summarized
        else:
            core_markets[market_clean] = summarized

    # En dengeli (%50-%50'ye en yakın) Ana Baremi (Main Line) bul
    def pick_main_and_key_lines(lines_dict: dict, limit: int = 5) -> dict:
        if not lines_dict:
            return {}
        sorted_lines = sorted(
            lines_dict.items(),
            key=lambda item: (item[1].get("balance_diff", 999), -item[1]["bookmaker_count"])
        )
        selected = dict(sorted_lines[:limit])
        main_line_key = sorted_lines[0][0]
        return {
            "main_line": main_line_key,
            "main_line_data": sorted_lines[0][1],
            "key_alternate_lines": selected,
        }

    clean_match["core_markets"] = core_markets
    clean_match["totals_summary"] = pick_main_and_key_lines(over_under_lines, limit=7)
    clean_match["spread_summary"] = pick_main_and_key_lines(handicap_lines, limit=7)
    return clean_match


def generate_markdown_report(optimized_matches: list[dict], date_str: str) -> str:
    """LLM'e doğrudan prompt olarak verilebilecek özet Markdown tablosu üretir."""
    lines = [
        f"# NBA Günlük İddaa/Bahis Piyasa Analiz Verisi ({date_str})",
        "",
        "> **AI Analiz Yönergesi:** Aşağıdaki veriler tüm bahis bürolarının oran ortalamalarını (`avg_odd`), piyasadaki en yüksek oranı (`max_odd`), büro kar marjından arındırılmış gerçek kazanma olasılığını (`fair_prob_pct`) ve bürolar arası standart sapmayı (`std_dev`) içerir. `std_dev` yüksekse bürolar arasında görüş ayrılığı vardır; `max_odd` ile `avg_odd` arasındaki fark açıksa 'Value Bet' (Değerli Oran) fırsatı mevcuttur.",
        ""
    ]

    for m in optimized_matches:
        home = m.get("home_team", "Ev Sahibi")
        away = m.get("away_team", "Deplasman")
        kickoff = m.get("kickoff") or m.get("match_date", "Belirsiz")
        lines.append(f"## 🏀 {home} vs {away} (Başlangıç: `{kickoff}`)")

        # Moneyline / 1X2
        for m_name, m_data in m.get("core_markets", {}).items():
            lines.append(f"### Market: `{m_name}` (Büro Sayısı: {m_data['bookmaker_count']} | Marj: %{m_data.get('market_margin_pct', 0)})")
            lines.append("| Seçenek | Ort. Oran | En Yüksek Oran (Büro) | Gerçek Olasılık (No-Vig) | Sapma (Std) |")
            lines.append("| :--- | :---: | :---: | :---: | :---: |")
            for out_k, out_v in m_data["outcomes"].items():
                lines.append(
                    f"| **{out_k}** | {out_v['avg_odd']} | **{out_v['max_odd']}** ({out_v['best_bookie']}) | **%{out_v.get('fair_prob_pct', 0)}** | {out_v['std_dev']} |"
                )
            lines.append("")

        # Ana Handikap ve Toplam Sayı Baremleri
        for section_key, title in [("spread_summary", "Handikap (Spread) Ana ve Kritik Baremler"), ("totals_summary", "Toplam Sayı (Over/Under) Ana ve Kritik Baremler")]:
            sec = m.get(section_key, {})
            if not sec:
                continue
            lines.append(f"### {title} (Ana Barem: `{sec['main_line']}`)")
            lines.append("| Barem | Seçenek | Ort. Oran | En Yüksek Oran | Gerçek Olasılık | Sapma |")
            lines.append("| :--- | :--- | :---: | :---: | :---: | :---: |")
            for l_key, l_data in sec.get("key_alternate_lines", {}).items():
                is_main = "⭐ " if l_key == sec["main_line"] else ""
                for out_k, out_v in l_data["outcomes"].items():
                    lines.append(
                        f"| {is_main}`{l_key}` | {out_k} | {out_v['avg_odd']} | {out_v['max_odd']} ({out_v['best_bookie']}) | %{out_v.get('fair_prob_pct', 0)} | {out_v['std_dev']} |"
                    )
            lines.append("")
        lines.append("---")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 4:
        print("Kullanım: python optimize_for_ai.py <ham_json> <cikti_json> <cikti_md> [tarih]")
        sys.exit(1)

    raw_path = Path(sys.argv[1])
    out_json_path = Path(sys.argv[2])
    out_md_path = Path(sys.argv[3])
    date_str = sys.argv[4] if len(sys.argv) > 4 else "Güncel"

    if not raw_path.exists():
        print(f"Uyarı: Ham veri dosyası bulunamadı ({raw_path}). Bugün maç olmayabilir.")
        sys.exit(0)

    with raw_path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if not isinstance(raw_data, list):
        raw_data = [raw_data]

    optimized = [optimize_match(match) for match in raw_data]

    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    with out_json_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "date": date_str,
                "match_count": len(optimized),
                "matches": optimized,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    md_content = generate_markdown_report(optimized, date_str)
    with out_md_path.open("w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"AI optimizasyonu tamamlandı: {len(optimized)} maç işlendi.")


if __name__ == "__main__":
    main()
