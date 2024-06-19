#21100011042 / NADİRE NUR SAĞLAM


import time
import cv2

import ElizlemeModulu as htm  # Sol el için parmak sayma modülü


# Sağ el için parmak sayma fonksiyonu
# Bu fonksiyon, sağ elin pozisyonunu ve parmaklarının durumunu belirler.

def parmak_say_sag(img):
    img = detector_sag.findHands(img) # Sağ elin konumunu bulmak için el algılama işlevini çağırır.

    lmList = detector_sag.findPosition(img, draw=False)
    # El algılama işlevi sonucunda elin landmark'larının pozisyonunu içeren bir liste elde edilir.
    # 'draw' parametresi, landmark'ların çizilip çizilmeyeceğini belirler.

    if lmList: # Eğer el algılama işlevi başarılı olduysa
        fingers = []  # Boş bir liste oluşturulur, bu liste parmakların durumunu saklayacak.

        # Baş parmağın pozisyonunu kontrol eder ve açılı olduğunu belirler.
        # Baş parmak, diğer parmaklardan farklı olarak sola doğru uzanmışsa, açıktır.

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1) # Eğer parmak açıksa, listeye 1 değerini ekler.
        else:
            fingers.append(0) # Eğer parmak kapalıysa, listeye 0 değerini ekler.

        # Diğer parmakların pozisyonunu kontrol eder ve eğik olup olmadıklarını belirler.
        # Eğer parmak, parmak ucundan biraz aşağıda ise, eğiktir.

        for id in range(1, 5):
            # y koordinatı bundan 2 aşağıda olan değerin altına indiyse parmak kapalı demektir.

            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1) # Toplam açık parmakların sayısını hesaplar.
        return totalFingers
    else:
        return 0 #el algılama başarısız olursa


# Sol el için parmak sayma algoritması
def parmak_say_sol(img):
    img = detector_sol.findHands(img)
    lmList = detector_sol.findPosition(img, draw=False)
    if lmList:
        fingers = []
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers = fingers.count(1)
        return totalFingers
    else:
        return 0
# Video akışını başlat
cap = cv2.VideoCapture(0)

# Video çerçevesinin boyutları
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Yeni boyutlar (çerçevenin büyütülmüş hali)
new_width = frame_width + 300
new_height = frame_height + 200

# Sağ el için bir el algılayıcı nesnesi oluşturuldu.
# detectionCon=1 parametresi algılama güvenilirliğini, maxHand=1 aynı anda max kaç el algılanabileceğini ayarlar.
detector_sag = htm.handDetector(detectionCon=1, maxHands=1)  # maxHands=1 sadece en yakın eli algılamak için
# Sol el için detector
detector_sol = htm.handDetector(detectionCon=1, maxHands=1)

tipIds = [4, 8, 12, 16, 20]  # parmak uçları
# Başlangıç zamanını al
start_time = time.time()
frames_processed = 0 # işlem sırasında işlenen kare sayısını tutar.
# FPS değerini ekranda tutmak için bir değişken oluştur
fps_display = "FPS: " #işlem sırasında ekrana fps(kare hızı) değerini göstermek için kullanılır.

while True: # video akışından kareler alır.
    ret, frame = cap.read()
    if not ret: # kare başarıyla alınamamışsa döngüden çıkar.
        break

    # Çerçevenin boyutunu büyüt
    frame = cv2.resize(frame, (new_width, new_height))

    # Görüntüyü BGR'den RGB'ye dönüştür
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Sağ ve sol elde parmak sayma
    total_fingers_sag = parmak_say_sag(frame) #frame adlı görüntüyü verir fonksiyona
    total_fingers_sol = parmak_say_sol(frame)

    # Toplam parmak sayısı
    total_fingers = total_fingers_sag + total_fingers_sol

    # Sağ ve sol eldeki parmak sayılarını ekrana yazdırma
    cv2.putText(frame, f'Sag El Parmak Sayisi: {total_fingers_sag}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Sol El Parmak Sayisi: {total_fingers_sol}', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255), 2, cv2.LINE_AA)
    # (20,120)-> metnin konumu, 1->metnin boyutu, 2->metnin kalınlığı, cv2.LINE_AA->metnin kenarlık tipi

    # Toplam parmak sayısını sol alt köşeye dikdörtgen içinde yazdırma
    cv2.rectangle(frame, (20, new_height - 200), (280, new_height - 50), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, str(total_fingers), (43, new_height - 60), cv2.FONT_HERSHEY_PLAIN,
                10, (0, 0, 255), 25)

    # FPS değerini ekranda gösterme
    cv2.putText(frame, fps_display, (frame_width,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Kare sayısını artır
    frames_processed += 1 #işlenen kare sayısı

    # FPS hesapla
    if time.time() - start_time >= 1: #1 sn de bir fps hesaplar.
        fps = frames_processed / (time.time() - start_time)
        # geçen sürede işlenen kare sayısının saniye cinsinden hesaplanmasıyla elde edilir.
        fps_display = f"FPS: {int(fps)}"
        # Başlangıç zamanını güncelle
        start_time = time.time()
        frames_processed = 0 #Yeni bir saniye başladığında, işlenen kare sayısını sıfırlar.

    cv2.imshow('Parmak Sayma', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Video akışını serbest bırak
cap.release()
cv2.destroyAllWindows()
