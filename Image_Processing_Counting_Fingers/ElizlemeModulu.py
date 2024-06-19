#21100011042 / NADİRE NUR SAĞLAM

import cv2
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        #Sınıfın başlatıcı metodudur. Bu metod, el tespiti için gerekli olan parametreleri alır ve sınıfın özelliklerini başlatır.
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        #Görüntüdeki elleri tespit etmek için kullanılır. Görüntüyü alır, el tespiti işlemini gerçekleştirir ve el tespit sonuçlarını döndürür.

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        # Görüntüde tespit edilen ellerin pozisyonunu belirlemek için kullanılır. Görüntüyü ve el numarasını (varsayılan olarak ilk el) alır, elin pozisyonunu belirler ve elin uç noktalarının koordinatlarını bir liste olarak döndürür.
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

    def flip_image(self, img):
        # Görüntüyü yatay olarak çevirme
        img = cv2.flip(img, 1)
        return img

    def swap_left_right(self, lmList):
        #Bu metod, eldeki landmark noktalarının koordinatlarını sol ve sağ el arasında değiştirir.
        # Sol elin koordinatlarını sağ elin koordinatlarına ve sağ elin koordinatlarını sol elin koordinatlarına değiştirir.

        # Sol ve sağ elin koordinatlarını değiştirme
        swapped_lmList = []
        for lm in lmList:
            id, cx, cy = lm
            # Yatay koordinatların işaretini tersine çevir
            cx = 1 - cx
            swapped_lmList.append([id, cx, cy])
        return swapped_lmList

