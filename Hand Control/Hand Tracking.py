import cv2 # pip install opencv-python
import serial # pip install pyserial
import mediapipe as mp
import time

# time.sleep(3)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

port_name = 'COM10'
baudrate = 115200
arduino = serial.Serial(port_name, baudrate=baudrate, timeout=0.1)

cap = cv2.VideoCapture(0)

# out = cv2.VideoWriter('hand tracking.mp4', -1, 20.0, (640,480))

def is_finger_up(hand):
    # Function to check if thumb is up
    finger_middle = hand.landmark[3].y
    finger_top = hand.landmark[4].y
    dist = max((finger_middle - finger_top),0) * 100
    return dist > 5

def get_thumb_custom_slope(hand):
    # Function to get distance between
    # middle joint & top tip of thumb
    finger_middle = hand.landmark[3].x
    finger_top = hand.landmark[4].x
    dist = (finger_middle - finger_top) * 100
    return dist

def is_finger_left(hand):
    # Function to check if thumb is p9ointing left
    dist = get_thumb_custom_slope(hand)
    # -5 < dist < 5
    # -2 is more sensitive than -3
    return dist <= -3

def is_finger_right(hand):
    # Function to check if thumb is pointing right
    dist = get_thumb_custom_slope(hand)
    # -5 < dist < 5
    # 2 is more sensitive than 3
    return dist >= 3

def send_arduino(message):
    # Function to send message to arduino
    arduino.write(bytes(message, 'utf-8')) 

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    if success:
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            all_hands = results.multi_hand_landmarks
            if len(all_hands) == 1:
                finger_is_up = is_finger_up(all_hands[0])
                finger_is_left = is_finger_left(all_hands[0])
                finger_is_right = is_finger_right(all_hands[0])

                if finger_is_left:
                    print("LEFT", end='\r')
                    command = 'a'
                elif finger_is_right:
                    print("RIGHT", end='\r')
                    command = 'd'
                elif finger_is_up:
                    print("UP", end='\r')
                    command = 'w'
                else:
                    print("NONE", end='\r')
                    command = 's'

                send_arduino(command)

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Flip the image horizontally for a selfie-view display.
        flipped_img = cv2.flip(image, 1)
        cv2.imshow('MediaPipe Hands', flipped_img)
#         out.write(flipped_img)

        if cv2.waitKey(2) & 0xFF == ord('q'):

          break
    else:
        break
    
cap.release()
# out.release()
cv2.destroyAllWindows()
send_arduino('s')
arduino.close()