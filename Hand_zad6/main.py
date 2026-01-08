"""
Hand gesture detection (MediaPipe Hands + OpenCV)

Opis:
    Program wykrywa dłoń na obrazie z kamery w czasie rzeczywistym
    i rozpoznaje prosty gest na podstawie liczby wyprostowanych palców
    (bez kciuka). Wynik jest wyświetlany jako tekst na ekranie.

Zasada działania:
    - OpenCV pobiera klatki z kamery (BGR).
    - Klatka jest konwertowana do RGB (MediaPipe wymaga RGB).
    - MediaPipe Hands wykrywa 21 punktów (landmarks) dłoni.
    - Dla każdego z 4 palców (index, middle, ring, pinky) sprawdzamy,
      czy palec jest wyprostowany:
        tip_y < pip_y
      ponieważ w obrazie współrzędna Y rośnie w dół (mniejsze Y = wyżej).
    - Liczba wyprostowanych palców (0–4) jest mapowana na gest:
        0 -> PAUSE
        1 -> NEXT
        2 -> PREV
        4 -> PLAY
        inne -> HOLD

Sterowanie:
    - ESC: zakończenie programu

Wymagania:
    - Python 3.11
    - opencv-python
    - mediapipe==0.10.14

Autorzy:
    s27433
    s28866

"""

import cv2
import mediapipe as mp

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Kamera
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # MediaPipe RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:

                # Rysuj punkty dłoni
                mp_draw.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                # --- LICZENIE PALCÓW  ---
                tips = [
                    mp_hands.HandLandmark.INDEX_FINGER_TIP, # 8
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP, # 12
                    mp_hands.HandLandmark.RING_FINGER_TIP, # 16
                    mp_hands.HandLandmark.PINKY_TIP #20
                ]

                count = 0
                for tip in tips:
                    tip_y = hand.landmark[tip].y
                    pip_y = hand.landmark[tip - 2].y  # PIP, zgiecie palca
                    if tip_y < pip_y:
                        count += 1
                print(hand.landmark)

                # --- MAPOWANIE NA GEST ---
                if count == 0:
                    gesture = "PAUSE"
                elif count == 1:
                    gesture = "NEXT"
                elif count == 2:
                    gesture = "PREV"
                elif count == 4:
                    gesture = "PLAY"
                else:
                    gesture = "HOLD"

                # Wyświetl gest
                cv2.putText(frame, f"GEST: {gesture} (palce={count})", (30, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)


        cv2.imshow("Wykrywanie gestow", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

cap.release()
cv2.destroyAllWindows()
