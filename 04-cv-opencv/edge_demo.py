import os
import cv2
import numpy as np

# 1) Sabitler
IMG_PATH = "04-cv-opencv/sample.jpg"  # varsa bunu kullan
OUT_PATH = "04-cv-opencv/edges.png"   # varsayılan çıktı

# 2) Görseli getir: varsa oku, yoksa sentetik üret
def make_synthetic():
    # 256x256 siyah tuval
    img = np.zeros((256, 256), dtype=np.uint8)
    # beyaz kare
    cv2.rectangle(img, (30, 30), (220, 220), 255, 3)
    # beyaz daire
    cv2.circle(img, (128, 128), 60, 225, 2)
    # yazı ekle
    cv2.putText(img, "DRONE", (85, 135),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, 225, 2)
    return img

if os.path.exists(IMG_PATH):
    img = cv2.imread(IMG_PATH, 0)  # 0 = grayscale okuma
    print(f"Görsel bulundu: {IMG_PATH} Boyut: {img.shape}")
else:
    print("Uyarı: sample.jpg yok, sentetik görsel oluşturuluyor.")
    img = make_synthetic()

# 3) Canny kenar tespiti - farklı eşik değerleri ile
thresholds = [
    (50, 150),
    (100, 200),
    (150, 300),
]

for t1, t2 in thresholds:
    edges = cv2.Canny(image=img, threshold1=t1, threshold2=t2)
    out_path = f"04-cv-opencv/edges_{t1}_{t2}.png"
    ok = cv2.imwrite(out_path, edges)
    print(("OK" if ok else "FAIL"), out_path)

# 4) Varsayılan çıktıyı da kaydet
edges_default = cv2.Canny(image=img, threshold1=100, threshold2=200)
cv2.imwrite(OUT_PATH, edges_default)
print(f"Tamam: {OUT_PATH} kaydedildi.")
