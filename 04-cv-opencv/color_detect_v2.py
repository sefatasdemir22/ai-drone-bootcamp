import cv2
import numpy as np
import argparse
import time
import os
from pathlib import Path

PRESETS = {
    "red": [((0, 120, 70), (10, 255, 255)), ((170, 120, 70), (180, 255, 255))],  # iki aralık
    "green": [((36, 40, 40), (89, 255, 255))],
    "blue": [((90, 40, 40), (128, 255, 255))],
}

def parse_hsv_range(s):
    # format: "lH,lS,lV:hH,hS,hV|lH2,lS2,lV2:hH2,hS2,hV2"
    parts = s.split("|")
    ranges = []
    for p in parts:
        low_str, high_str = p.split(":")
        lo = tuple(int(x) for x in low_str.split(","))
        hi = tuple(int(x) for x in high_str.split(","))
        ranges.append((lo, hi))
    return ranges
#s olarak girilen değeri önce | ile girer ve onu splitle parts içine atarız.
#sonra ranges boş listesi belirleyip döngüye gireriz parts içindeki her değer için : ile ayırırız low ve high olarak.
#sonrasında bunları tuple olarak tutarız her virgülde ayırıp.
#en son ranges listesine ekleriz.

def build_mask(hsv, ranges):
    mask_total = None
    for r in ranges:
        lo, hi = r
        m = cv2.inRange(hsv, np.array(lo, np.uint8), np.array(hi, np.uint8))
        mask_total = m if mask_total is None else cv2.bitwise_or(mask_total, m)
    return mask_total
#Henüz maske yok, bu yüzden None ile başlıyoruz.
#ranges → HSV aralıklarının listesi (örn. kırmızı için 2 aralık).
#Döngüyle her lo ve hi (alt-üst sınır) alınır.
#cv2.inRange → HSV değerleri lo ve hi arasında olan pikselleri beyaz (255) yapar, diğerlerini siyah (0).
#Yani sadece istediğimiz renk aralığını ayıklar.
#np.uint8 → OpenCV’nin doğru formatta çalışması için.
#cv2.inRange() = renk filtresi. Aralık içindekiler beyaz, diğerleri siyah.
#np.array(lo, np.uint8) = HSV sınırlarını NumPy array + doğru veri tipi yapıyoruz.
#np.uint8 = her kanal 0–255 arası tutulduğu için.

#Eğer daha önce maske varsa, yeni maskeyi eskiyle OR (veya) işlemiyle birleştir.
#Eğer herhangi biri beyaz (255) → sonuç beyaz.  bitwise_or = piksel bazlı mantıksal veya.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", type=str, help="Color preset: red, green, blue")
    parser.add_argument("--file", type=str, help="Image file path (optional)")
    args = parser.parse_args()

    if args.preset and args.preset in PRESETS:
        ranges = PRESETS[args.preset]
    else:
        print("Preset bulunamadı. Varsayılan kırmızı seçildi.")
        ranges = PRESETS["red"]
        #hata olmaması için bir şey girilmezse varsayılan olarak kırmızı seçiyoruz

    # Kamera veya dosya mı kontrol etme
    if args.file: #eğer dosya varsa burada onu açmaya çalışır.
        frame = cv2.imread(args.file)
        if frame is None:
            print("Dosya okunamadı:", args.file)
            return #hata verir ve burdan çıkar.
    else: #dosya yoksa kamera açmaya çalışır.
        cap = cv2.VideoCapture(0)
        if not cap.isOpened(): #açıldı mı kontrol eder.
            print("Kamera bulunamadı")
            return

        while True: #kamera açıkken döngü.
            ret, frame = cap.read() #kameradan bir frame alır
            if not ret: #true ise görüntü alındı false ise hata oldu
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #görüntüyü bgrden hsvye çeviriyoruz.
            mask = build_mask(hsv, ranges) #daha önceki fonksiyonla istediğimiz rengi siyah beyaz maskeye dönüştürüyoruz.
            

            result = cv2.bitwise_and(frame, frame, mask=mask)# maskeyi orijinal görüntüye uygula. Sadece istediğimiz renk görünür diğerleri siyah olur.
          

            cv2.imshow("Original", frame) #kameradan gelen işlenmemiş görüntü
            cv2.imshow("Mask", mask) # siyah-beyaz maske
            cv2.imshow("Result", result) # Sadece istediğimiz rengi gösteren sonuç.

            if cv2.waitKey(1) & 0xFF == ord("q"): #klavyeden tuş dinler, q tuşunun ASCII değeri uygulanırsa döngüden çıkılır kamera kapanır.
                break

        cap.release() #kamera bağlantısını serbest bırakır.
        cv2.destroyAllWindows() #tüm pencereleri kapatır.
        return

    # Dosya üzerinden test yapılıyorsa eğer.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = build_mask(hsv, ranges)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
