# PX4 + MAVSDK Senaryoları

Bu klasörde PX4 SITL simülasyonu ile MAVSDK tabanlı uçuş senaryoları yer almaktadır.  
Senaryolar Gazebo ortamında test edilmiştir.  

## 🚀 Uçuş Senaryoları

### 1. Kare Uçuş Testi
- **Amaç:** Drone’un Gazebo ortamında kare çizerek uçuş yapması.
- **Kod:** [`square_flight.py`](square_flight.py)
- **Adımlar:**
  1. 3 metreye kalkış
  2. İleri (x=5m)
  3. Sağa (y=5m)
  4. Geri (x=0)
  5. Sola (y=0)
  6. İniş

### 2. Görsel Kontrollü Uçuş (Vision Control)
- **Amaç:** Drone’un kamera ile algıladığı **yeşil nesneye göre hareket etmesi.**
- **Kod:** [`vision_control.py`](vision_control.py)
- **Kontrol Mantığı:**
  - Nesne **soldaysa** → sola
  - Nesne **sağdaysa** → sağa
  - Nesne **ortadaysa** → ileri
  - Nesne **yoksa** → hover (bekleme)

> ⚠️ Bu senaryo demo amaçlıdır. İleri sürümlerde PID tabanlı kontrol, geri hareket, farklı renkler ve nesne algılama (YOLO, Mediapipe) desteği eklenecektir.

