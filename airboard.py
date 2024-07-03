import cv2 as cv
import numpy as np
import mediapipe as mp
import time

# Initialize MediaPipe hand detection
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# Open video capture
video = cv.VideoCapture(0)

# Create a whiteboard image
whiteboard = np.ones((480, 640, 3), np.uint8) * 255

# Variables to store the previous position of the finger
prev_x, prev_y = None, None
smoothed_x, smoothed_y = None, None
alpha = 0.3  # Reduced smoothing factor for more responsiveness

# Timer variables
last_draw_time = time.time()
line_break_threshold = 3  # Time in seconds to break the line

# Color options
colors = {
    'k': (0, 0, 0),   # Black
    'r': (0, 0, 255), # Red
    'b': (255, 0, 0), # Blue
    'g': (0, 255, 0)  # Green
}
current_color = (0, 0, 0)  # Initial color (black)

def are_fingers_up(landmarks):
    """Check if all fingers are up based on landmark positions."""
    tips = [4, 8, 12, 16, 20]
    mcp = [2, 5, 9, 13, 17]

    fingers_up = [landmarks[tip].y < landmarks[mc].y for tip, mc in zip(tips, mcp)]

    return all(fingers_up)

while True:
    try:
        isTrue, frame = video.read()
        if not isTrue:
            break

        # Flip the frame horizontally for a natural experience
        frame = cv.flip(frame, 1)

        # Convert the frame to RGB
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Flag to check if the palm is detected
        palm_detected = False
        drawing = True

        if results.multi_hand_landmarks:
            for hlms in results.multi_hand_landmarks:
                # Draw hand landmarks
                mpDraw.draw_landmarks(frame, hlms, mpHands.HAND_CONNECTIONS)

                # Get coordinates for index finger tip
                index_finger_tip = hlms.landmark[8]
                h, w, c = frame.shape
                cx_tip, cy_tip = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                # Apply smoothing using exponential moving average
                if smoothed_x is None and smoothed_y is None:
                    smoothed_x, smoothed_y = cx_tip, cy_tip
                else:
                    smoothed_x = alpha * cx_tip + (1 - alpha) * smoothed_x
                    smoothed_y = alpha * cy_tip + (1 - alpha) * smoothed_y

                # Check if all fingers are up
                if are_fingers_up(hlms.landmark):
                    palm_detected = True

                # If the previous coordinates are not None and palm is not detected, draw a line
                if prev_x is not None and prev_y is not None and not palm_detected:
                    cv.line(whiteboard, (int(prev_x), int(prev_y)), (int(smoothed_x), int(smoothed_y)), current_color, 5)
                    drawing = True

                # Update previous coordinates
                prev_x, prev_y = smoothed_x, smoothed_y

                # If the index finger is not up, reset the previous coordinates and drawing state
                index_finger_base = hlms.landmark[5]
                if index_finger_tip.y > index_finger_base.y:
                    prev_x, prev_y = None, None
                    drawing = False

        # If no drawing for the threshold time, break the line
        if not drawing and time.time() - last_draw_time > line_break_threshold:
            prev_x, prev_y = None, None

        # If palm is detected, clear the whiteboard and reset drawing timer
        if palm_detected:
            whiteboard = np.ones((480, 640, 3), np.uint8) * 255
            last_draw_time = time.time()  # Reset draw timer

        key_instructions = "Press 'k' for black, 'r' for red, 'b' for blue, 'g' for green | Press 'q' to quit"
        cv.putText(frame, key_instructions, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.70, (0, 0, 0), 1, cv.LINE_AA)
        # Display the frame in the main window
        cv.imshow("Live Feed", frame)

        # Display the whiteboard in a separate window
        cv.imshow("Whiteboard", whiteboard)

        # User input to change color
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif chr(key) in colors:
            current_color = colors[chr(key)]

    except Exception as e:
        print(f"Exception occurred: {e}")
        break

# Release video capture and close all windows
video.release()
cv.destroyAllWindows()
