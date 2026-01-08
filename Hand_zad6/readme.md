# Hand Gesture Detection (MediaPipe + OpenCV)

 **Prosty system rozpoznawania gestów dłoni** w czasie rzeczywistym z kamery, wykorzystujący:
- **MediaPipe Hands** – detekcja dłoni i 21 landmarków
- **OpenCV** – kamera i wizualizacja

Gesty są rozpoznawane na podstawie liczby wyprostowanych palców (bez kciuka).

---

##  Gif


![Demo działania aplikacji](hand_loop.gif)


---

##  Funkcjonalności

| Liczba palców | Rozpoznany gest |
|---------------|-----------------|
| 0             | `PAUSE`         |
| 1             | `NEXT`          |
| 2             | `PREV`          |
| 4             | `PLAY`          |


---

##  Jak działa

1. OpenCV pobiera obraz z kamery (BGR).
2. Obraz konwertowany jest do RGB (wymagane przez MediaPipe).
3. MediaPipe wykrywa dłoń i 21 punktów.
4. Porównywane są wysokości TIP vs PIP (dla 4 palców).
5. Na tej podstawie rozpoznawany jest gest.

---

##  Wymagania

- **Python 3.11**
- `opencv-python`
- `mediapipe==0.10.14`

---

## Autorzy

s27433, s28866

---
