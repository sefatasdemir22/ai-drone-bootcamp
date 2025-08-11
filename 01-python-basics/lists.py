# Liste oluşturma ve işlem yapma
drone_modelleri = ["DJI Mini 3", "Parrot Anafi", "Skydio 2"]

print("Mevcut dronelar:", drone_modelleri)

drone_modelleri.append("DJI Avata") #listeye ekleme
print("Yeni Liste:", drone_modelleri)

drone_modelleri.remove("Parrot Anafi") #listeden silme
print("Silme sonrasi:" , drone_modelleri)

print("Ilk iki drone:", drone_modelleri[0:2]) #dilimleme

