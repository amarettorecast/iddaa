#!/usr/bin/env python3
"""OddsHarvester JSON çıktısını AI'ın okuyabileceği kompakt özete çevirir.

Kullanım: python scripts/optimize.py <raw.json> <çıktı_klasörü>

Her maç / market için bookmaker oranlarının medyanı, en iyi oran,
marj ve marjdan arındırılmış olasılık hesaplanır. Çıktı:
  summary.json  -> makine okur
  summary.md    -> AI'a yapıştırılacak metin (prompt dahil)

Not: Girdi şeması README'ye göre savunmacı biçimde okunur. İlk çalıştırmada
summary.md'nin dolu çıktığını kontrol et.
"""
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

NON_ODDS = {"bookmaker_name", "bookmaker", "blocked_outcomes", "period"}
LINE_KEY = re.compile(r"(handicap|hcp|line)", re.I)
META_KEYS = ("match_date", "league", "home_team", "away_team")
MAX_LINES_PER_MARKET = 3

PROMPT = """# Görev
Aşağıdaki veriler bugünün maçları için bahis şirketi oranlarının özetidir.
- med: bookmaker oranlarının medyanı, best: en yüksek oran
- p: marj çıkarıldıktan sonraki piyasa olasılığı, marj: bahis şirketi payı
- 1x2: 1=ev sahibi, X=beraberlik, 2=deplasman

Kurallar:
1. Sadece bu veriyi kullan, maç sonucu uydurma, takım bilgisi ekleme.
2. Piyasa olasılığı ile best oranı kıyasla; best oran medyandan belirgin yüksekse işaretle.
3. Düşük marjlı ve bookmaker sayısı yüksek marketleri daha güvenilir say.
4. Kesin tahmin verme; her önerinin olasılığını ve belirsizliğini yaz.
5. Çok maçlı kuponun toplam olasılığını (p'lerin çarpımı) hesapla ve göster.

"""


def num(v):
    try:
        return float(str(v).strip().replace(",", "."))
    except ValueError:
        return None


def is_line_key(k):
    return bool(LINE_KEY.search(k)) and not k.lower().startswith("odds")


def market_rows(match):
    for key, val in match.items():
        if (
            isinstance(val, list)
            and val
            and all(isinstance(x, dict) for x in val)
            and any("bookmaker_name" in x for x in val)
        ):
            yield key, val


def analyze(rows):
    lines = defaultdict(lambda: defaultdict(list))
    for r in rows:
        blocked = {str(b) for b in (r.get("blocked_outcomes") or [])}
        line = next((str(v) for k, v in r.items() if is_line_key(k)), "")
        for k, v in r.items():
            if k in NON_ODDS or k in blocked or is_line_key(k):
                continue
            o = num(v)
            if o is not None and o > 1.0:
                lines[line][k].append(o)

    out = []
    for line, outcomes in lines.items():
        if len(outcomes) < 2:
            continue
        med = {k: statistics.median(v) for k, v in outcomes.items()}
        inv = {k: 1 / o for k, o in med.items()}
        s = sum(inv.values())
        out.append(
            {
                "line": line or None,
                "books": max(len(v) for v in outcomes.values()),
                "margin_pct": round((s - 1) * 100, 1),
                "outcomes": {
                    k: {
                        "med": round(med[k], 2),
                        "best": round(max(outcomes[k]), 2),
                        "p": round(inv[k] / s, 3),
                    }
                    for k in med
                },
            }
        )

    if len(out) > MAX_LINES_PER_MARKET:
        # En dengeli (en bilgilendirici) çizgileri tut
        out.sort(
            key=lambda g: max(o["p"] for o in g["outcomes"].values())
            - min(o["p"] for o in g["outcomes"].values())
        )
        out = out[:MAX_LINES_PER_MARKET]
    return out


def load(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for k in ("matches", "data", "results"):
            if isinstance(data.get(k), list):
                return data[k]
        return [data]
    return data


def build(matches):
    res, skipped = [], 0
    for m in matches:
        if not isinstance(m, dict):
            continue
        markets = {}
        for name, rows in market_rows(m):
            a = analyze(rows)
            if a:
                markets[name.removesuffix("_market")] = a
        if not markets:
            skipped += 1
            continue
        item = {k: m.get(k) for k in META_KEYS}
        item["markets"] = markets
        res.append(item)
    res.sort(key=lambda x: str(x.get("match_date")))
    return res, skipped


def render_md(matches):
    out = [PROMPT, f"# Veri ({len(matches)} maç)\n"]
    for m in matches:
        out.append(
            f"## {m['home_team']} - {m['away_team']} | {m['league']} | {m['match_date']}"
        )
        for name, groups in m["markets"].items():
            for g in groups:
                tag = name + (f" [{g['line']}]" if g["line"] else "")
                parts = " | ".join(
                    f"{k} {v['med']:.2f} (en iyi {v['best']:.2f}, p %{v['p'] * 100:.0f})"
                    for k, v in g["outcomes"].items()
                )
                out.append(f"- {tag} marj %{g['margin_pct']} ({g['books']} bk): {parts}")
        out.append("")
    return "\n".join(out)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    raw_path, out_dir = sys.argv[1], Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    matches, skipped = build(load(raw_path))
    if not matches:
        print("::warning::Oran verisi içeren maç bulunamadı (şema farklı olabilir).")

    (out_dir / "summary.json").write_text(
        json.dumps(matches, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    (out_dir / "summary.md").write_text(render_md(matches), encoding="utf-8")
    print(f"{len(matches)} maç yazıldı, {skipped} maç oransız atlandı.")


if __name__ == "__main__":
    main()
