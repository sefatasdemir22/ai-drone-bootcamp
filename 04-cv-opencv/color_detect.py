import os
import cv2
import numpy as np

IMG_PATH = "04-cv-opencv/sample.jpg"

# 1) Görseli hazırla
img = cv2.imread(IMG_PATH)
if img is None:
    print("Uyari: sample.jpg yok, sentetik gorsel olusturuluyor.")
    img = np.zeros((256, 256, 3), dtype=np.uint8)        # siyah zemin
    cv2.circle(img, (128, 128), 60, (0, 0, 255), -1)     # BGR kirmizi daire

# 2) BGR -> HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 3) Kirmizi araliklari
lower_red1 = np.array([0,   120, 70], dtype=np.uint8)
upper_red1 = np.array([10,  255, 255], dtype=np.uint8)
lower_red2 = np.array([170, 120, 70], dtype=np.uint8)
upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask  = cv2.bitwise_or(mask1, mask2)

# 4) Maskeyi uygula
res = cv2.bitwise_and(img, img, mask=mask)

# 5) Maske temizligi
mask_clean = cv2.GaussianBlur(mask, (5, 5), 0)
kernel = np.ones((3, 3), np.uint8)
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_OPEN,  kernel, iterations=1)
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel, iterations=1)

# 5.1) findContours icin kesin ikili hale getir
_, mask_bin = cv2.threshold(mask_clean, 127, 255, cv2.THRESH_BINARY)

# 6) Kontur + kutu
contours, _ = cv2.findContours(mask_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
boxed = img.copy()
if contours:
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)   # en dis dikdortgen
    cv2.rectangle(boxed, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(f"En buyuk kontur: x={x}, y={y}, w={w}, h={h}")
else:
    print("Kontur bulunamadi.")

# 7) Goster/Kaydet
try:
    cv2.imshow("Orijinal", img)
    cv2.imshow("Maske (Kirmizi)", mask)
    cv2.imshow("Sonuc", res)
    cv2.imshow("Kutulu", boxed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print("imshow acilamadi, dosyaya kayit yapiliyor:", e)

ok1 = cv2.imwrite("04-cv-opencv/red_mask.png",   mask)
ok2 = cv2.imwrite("04-cv-opencv/red_result.png", res)
ok3 = cv2.imwrite("04-cv-opencv/red_boxed.png",  boxed)
print("Kaydedildi:" if (ok1 and ok2 and ok3) else "Kayit hatasi",
      "red_mask.png, red_result.png, red_boxed.png")
