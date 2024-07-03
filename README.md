# Airboard: Interactive Virtual Whiteboard

Airboard is an interactive virtual whiteboard project built using Python, OpenCV, and MediaPipe. It allows users to draw on a virtual canvas using hand gestures captured through a webcam.

## Overview

Airboard utilizes hand tracking and gesture recognition to interpret hand movements as drawing actions on a computer screen. It supports multiple colors and erasing functionalities based on hand gestures.

## Features

- Real-time hand tracking using MediaPipe.
- Gesture recognition for drawing lines.
- Supports multiple drawing colors (black, red, blue, green).
- Erasing functionality by opening the palm.
- Simple keyboard interaction for color selection and quitting the application.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ADITYA2124/AIRBOARD.git
    ```

2. **Install dependencies:**

    ```bash
    pip install opencv-python mediapipe numpy
    ```

## Usage

1. **Run the script:**

    ```bash
    python airboard.py
    ```

2. **Interact with Airboard:**

    - Hold your hand in front of the webcam to start tracking.
    - Use index finger to draw lines in the selected color.
    - Open yuor palm  to erase the canvas.
    - Press keys 'k' for black, 'r' for red, 'b' for blue, 'g' for green to change drawing color.
    - Press 'q' to quit the application.

## Files

- `airboard.py`: Main script for running the Airboard application.
- `README.md`: Documentation and setup instructions.

## Demonstration

![Demonstration](https://github.com/ADITYA2124/AIRBOARD/assets/118548905/da5fbc37-2818-476a-8ec6-1fd61b8634e8)

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
