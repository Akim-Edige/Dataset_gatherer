# Hand Gesture dataset gathering with Flask

# **Project Overview**
This project is a simple Flask-based web application for capturing and processing hand gestures using **Mediapipe**. It allows users to upload images or videos, detect hand gestures, and save them into a dataset for further processing or model training. The system also visualizes the detected hand landmarks on images.

---

## **Features**

### **Image Capturing** ###:
- Review and retake the taken image
- Automatically annotate the image, and write coordinates of points in a json file.
- Writes metadata.csv with file name, sign and timestamp
- Visualize the detected hand landmarks
- Save only after reviewing and clicking corresponding button

### **Video Capturing**
- Captures and saves video in .webm format
---
## Project Structure

```

project/
│
├── app/
│   ├── __init__.py             # Initialize Flask app and register blueprints
│   ├── routes.py               # All route definitions
│   ├── utils.py                # Helper functions (image processing, keypoints extraction)
│   ├── config.py               # Configuration (paths, constants)
│   ├── templates/              # HTML files (index.html)
│   └── static/                 # Static files (JS)
│
├── tests/
│   ├── __init__.py
│   ├── sample_photo.txt
│   ├── sample_video.txt
│   ├── test_routes.py
│
├── run.py                      # Main entry point to start the app
└── requirements.txt            # Project dependencies

```

---

## Installation and Setup

Follow the steps below to install and run the project locally:

### Prerequisites

Make sure you have the following installed on your system:
- Python 3.7+
- pip (Python package installer)

### Steps

1. **Clone the repository**

   Open your terminal or command prompt and run the following command to clone the repository:

   ```bash
   git clone https://github.com/Akim-Edige/Dataset_gatherer.git
   cd Dataset_gatherer
   ```
2. **Create and activate the virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. ** Install the requirements**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the application**
  ```bash
  python3 app.py
   ```



