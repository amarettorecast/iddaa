# Görev
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


# Veri (2 maç)

## Frosinone - Lecce | None | 2026-10-29 17:30:00 UTC
- 1x2 marj %5.5 (8 bk): 1 1.71 (en iyi 1.77, p %55) | X 4.15 (en iyi 4.40, p %23) | 2 4.33 (en iyi 4.40, p %22)
- btts marj %7.8 (7 bk): btts_yes 1.40 (en iyi 1.42, p %66) | btts_no 2.75 (en iyi 2.85, p %34)
- over_under_0_5 marj %3.4 (4 bk): odds_over 1.02 (en iyi 1.03, p %95) | odds_under 18.75 (en iyi 19.00, p %5)
- over_under_1_5 marj %6.2 (6 bk): odds_over 1.10 (en iyi 1.13, p %85) | odds_under 6.38 (en iyi 7.00, p %15)
- over_under_1_75 marj %6.2 (2 bk): odds_over 1.12 (en iyi 1.13, p %84) | odds_under 5.90 (en iyi 5.90, p %16)
- over_under_2 marj %5.1 (3 bk): odds_over 1.15 (en iyi 1.16, p %83) | odds_under 5.50 (en iyi 5.50, p %17)
- over_under_2_25 marj %7.5 (2 bk): odds_over 1.26 (en iyi 1.27, p %74) | odds_under 3.55 (en iyi 3.55, p %26)
- over_under_2_5 marj %5.8 (6 bk): odds_over 1.40 (en iyi 1.42, p %68) | odds_under 2.91 (en iyi 3.00, p %32)
- over_under_2_75 marj %6.7 (2 bk): odds_over 1.46 (en iyi 1.48, p %64) | odds_under 2.60 (en iyi 2.60, p %36)
- over_under_3 marj %5.8 (3 bk): odds_over 1.58 (en iyi 1.60, p %60) | odds_under 2.35 (en iyi 2.35, p %40)
- over_under_3_25 marj %6.3 (2 bk): odds_over 1.77 (en iyi 1.78, p %53) | odds_under 2.01 (en iyi 2.03, p %47)
- over_under_3_5 marj %6.6 (7 bk): odds_over 1.96 (en iyi 2.03, p %48) | odds_under 1.80 (en iyi 1.83, p %52)
- over_under_3_75 marj %6.4 (2 bk): odds_over 2.25 (en iyi 2.25, p %42) | odds_under 1.61 (en iyi 1.63, p %58)
- over_under_4 marj %6.5 (3 bk): odds_over 2.60 (en iyi 2.65, p %36) | odds_under 1.47 (en iyi 1.48, p %64)
- over_under_4_25 marj %6.6 (2 bk): odds_over 3.00 (en iyi 3.00, p %31) | odds_under 1.36 (en iyi 1.38, p %69)
- over_under_4_5 marj %6.7 (6 bk): odds_over 3.17 (en iyi 3.40, p %30) | odds_under 1.33 (en iyi 1.35, p %70)
- over_under_4_75 marj %7.3 (2 bk): odds_over 3.80 (en iyi 3.80, p %24) | odds_under 1.23 (en iyi 1.25, p %76)
- over_under_5 marj %5.5 (3 bk): odds_over 5.00 (en iyi 5.00, p %19) | odds_under 1.17 (en iyi 1.17, p %81)
- over_under_5_25 marj %6.3 (2 bk): odds_over 5.50 (en iyi 5.50, p %17) | odds_under 1.14 (en iyi 1.15, p %83)
- over_under_5_5 marj %5.9 (6 bk): odds_over 5.50 (en iyi 5.60, p %17) | odds_under 1.14 (en iyi 1.15, p %83)
- over_under_6 marj %4.8 (1 bk): odds_over 10.50 (en iyi 10.50, p %9) | odds_under 1.05 (en iyi 1.05, p %91)
- over_under_6_5 marj %5.0 (4 bk): odds_over 10.75 (en iyi 11.00, p %9) | odds_under 1.04 (en iyi 1.06, p %91)
- over_under_7_5 marj %3.8 (3 bk): odds_over 21.00 (en iyi 21.00, p %5) | odds_under 1.01 (en iyi 1.02, p %95)

## Fiorentina - Atalanta | None | 2026-10-29 19:45:00 UTC
- 1x2 marj %5.8 (8 bk): 1 2.30 (en iyi 2.40, p %41) | X 3.65 (en iyi 3.80, p %26) | 2 2.87 (en iyi 2.90, p %33)
- btts marj %8.0 (7 bk): btts_yes 1.47 (en iyi 1.50, p %63) | btts_no 2.50 (en iyi 2.60, p %37)
- over_under_0_5 marj %4.2 (4 bk): odds_over 1.02 (en iyi 1.03, p %94) | odds_under 15.00 (en iyi 15.00, p %6)
- over_under_1 marj %3.6 (1 bk): odds_over 1.04 (en iyi 1.04, p %93) | odds_under 13.50 (en iyi 13.50, p %7)
- over_under_1_25 marj %6.0 (2 bk): odds_over 1.09 (en iyi 1.10, p %86) | odds_under 7.00 (en iyi 7.00, p %14)
- over_under_1_5 marj %6.2 (5 bk): odds_over 1.16 (en iyi 1.17, p %81) | odds_under 5.00 (en iyi 5.50, p %19)
- over_under_1_75 marj %7.1 (2 bk): odds_over 1.19 (en iyi 1.20, p %79) | odds_under 4.40 (en iyi 4.40, p %21)
- over_under_2 marj %6.3 (3 bk): odds_over 1.24 (en iyi 1.24, p %76) | odds_under 3.90 (en iyi 4.00, p %24)
- over_under_2_25 marj %7.3 (2 bk): odds_over 1.39 (en iyi 1.40, p %67) | odds_under 2.85 (en iyi 2.85, p %33)
- over_under_2_5 marj %6.5 (5 bk): odds_over 1.55 (en iyi 1.57, p %61) | odds_under 2.38 (en iyi 2.45, p %39)
- over_under_2_75 marj %7.0 (2 bk): odds_over 1.69 (en iyi 1.70, p %56) | odds_under 2.10 (en iyi 2.10, p %44)
- over_under_3 marj %5.3 (3 bk): odds_over 1.88 (en iyi 1.93, p %50) | odds_under 1.92 (en iyi 1.93, p %50)
- over_under_3_25 marj %7.0 (2 bk): odds_over 2.10 (en iyi 2.10, p %44) | odds_under 1.69 (en iyi 1.70, p %56)
- over_under_3_5 marj %6.7 (6 bk): odds_over 2.35 (en iyi 2.38, p %40) | odds_under 1.56 (en iyi 1.60, p %60)
- over_under_3_75 marj %7.0 (2 bk): odds_over 2.75 (en iyi 2.75, p %34) | odds_under 1.42 (en iyi 1.43, p %66)
- over_under_4 marj %5.9 (3 bk): odds_over 3.45 (en iyi 3.45, p %27) | odds_under 1.30 (en iyi 1.31, p %73)
- over_under_4_25 marj %7.3 (2 bk): odds_over 3.80 (en iyi 3.80, p %24) | odds_under 1.23 (en iyi 1.25, p %76)
- over_under_4_5 marj %6.4 (5 bk): odds_over 4.10 (en iyi 4.33, p %23) | odds_under 1.22 (en iyi 1.25, p %77)
- over_under_4_75 marj %6.4 (2 bk): odds_over 5.25 (en iyi 5.25, p %18) | odds_under 1.15 (en iyi 1.16, p %82)
- over_under_5 marj %5.2 (3 bk): odds_over 7.00 (en iyi 7.00, p %14) | odds_under 1.10 (en iyi 1.10, p %86)
- over_under_5_5 marj %5.7 (4 bk): odds_over 7.88 (en iyi 8.00, p %12) | odds_under 1.08 (en iyi 1.08, p %88)
- over_under_6_5 marj %3.9 (3 bk): odds_over 17.00 (en iyi 17.00, p %6) | odds_under 1.02 (en iyi 1.02, p %94)
- over_under_7_5 marj %2.5 (2 bk): odds_over 29.00 (en iyi 29.00, p %3) | odds_under 1.01 (en iyi 1.01, p %97)
