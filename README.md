# Oda Sıcaklığı Dashboard

Bu proje, oda sıcaklığı ve çeşitli sensör verilerini görselleştiren ve analiz eden bir Streamlit dashboard'udur.

## Özellikler

- 📊 Gerçek zamanlı veri görselleştirme
- 🔍 Anomali tespiti (Z-score tabanlı)
- 📈 Trend analizi (Hareketli ortalama)
- 🌡️ Çoklu sensör desteği (Sıcaklık, Işık, CO2, Hareket, Nem)
- 🎨 Modern ve kullanıcı dostu arayüz

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/yourusername/oda-sicakligi-dashboard.git
cd oda-sicakligi-dashboard
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı çalıştırın:
```bash
streamlit run main.py
```

## Geliştirme

### Kod Standartları
- PEP 8 kod stil rehberini takip edin
- Her yeni özellik için ayrı branch oluşturun
- Pull request'lerde en az bir reviewer onayı alın

### Test
```bash
# Testleri çalıştırın
pytest

# Kod kalitesi kontrolü
flake8
```

## CI/CD Pipeline

Proje GitHub Actions ile sürekli entegrasyon ve dağıtım süreçlerini kullanmaktadır:

1. **Test Pipeline**: Her push ve pull request'te çalışır
   - Python versiyonları testi (3.8, 3.9, 3.10)
   - Kod kalitesi kontrolü (flake8)
   - Unit testler

2. **Deployment Pipeline**: Main branch'e merge edildiğinde çalışır
   - Streamlit Cloud'a otomatik deploy
   - Versiyon numarası güncelleme
   - Changelog oluşturma

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın. 