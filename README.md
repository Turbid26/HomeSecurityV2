---

# 🏠 Home Security System V2

### Real-Time IoT Surveillance with AI and Sensor-Based Alerts

---

## 📌 Overview

**HomeSecurityV2** is a real-time IoT-based security system that combines **camera surveillance, AI-based detection, and sensor monitoring**.

The system uses an **ESP32-CAM for video streaming**, **Arduino with sensors (PIR, smoke, fire)** for environmental monitoring, and a **Flask backend with OpenCV** for detection. All events are synced to the cloud using Firebase, enabling real-time alerts and tracking.

---

## 🚀 Features

* 📷 Live video streaming from ESP32-CAM
* 🧠 Face detection and recognition using OpenCV
* 🚨 Unknown face detection with alerts
* 🔥 Fire, smoke, and motion detection using sensors
* ⚡ Real-time sensor updates via Firebase
* ☁️ Cloud storage using Cloudinary
* 📡 Event-driven alert system
* 🌐 Web interface for monitoring

---

## 🏗️ Architecture

```id="u2xk7z"
ESP32-CAM (Video Stream)
        ↓
Flask Backend (Processing)
        ↓
OpenCV (Face Detection)
        ↓
Firebase (Alerts + Sensor Data)
        ↑
Arduino (PIR, Smoke, Fire Sensors)
        ↓
Cloudinary (Image Storage)
```

---

## 🔁 Workflow

### Camera Pipeline

1. ESP32-CAM streams live video
2. Flask server receives frames
3. OpenCV performs detection
4. Unknown faces trigger alerts
5. Images are stored in Cloudinary

### Sensor Pipeline

1. Arduino reads PIR, smoke, and fire sensors
2. Sensor data is pushed to Firebase in real time
3. Alerts are triggered based on thresholds
4. Frontend reflects live updates

---

## 🧰 Tech Stack

### Hardware

* ESP32-CAM
* Arduino
* PIR Sensor (motion detection)
* Smoke Sensor
* Fire Sensor

### Backend

* Python
* Flask

### Computer Vision

* OpenCV
* Face Recognition

### Cloud & Storage

* Firebase (Realtime DB + Alerts)
* Cloudinary

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash id="g7t7hv"
git clone https://github.com/Turbid26/HomeSecurityV2
cd HomeSecurityV2
```

---

### 2. Setup Python Environment

```bash id="l8z2s1"
python -m venv venv
source venv/bin/activate
```

```bash id="d8y2qf"
pip install -r requirements.txt
```

---

### 3. Setup ESP32-CAM

* Upload camera streaming code using Arduino IDE
* Connect to WiFi
* Copy stream URL

---

### 4. Setup Arduino Sensors

* Connect:

  * PIR → Motion detection
  * Smoke sensor → Gas detection
  * Fire sensor → Flame detection

* Upload Arduino code to push sensor data to Firebase

---

### 5. Configure Environment

Create `.env`:

```id="q9t0aa"
FIREBASE_CONFIG=your_config
CLOUDINARY_URL=your_cloudinary_url
CAMERA_URL=your_stream_url
```

---

### 6. Run Application

```bash id="8i7cpx"
python app.py
```

Open:

```
http://localhost:5000
```

---

## 📡 System Capabilities

* Real-time video + sensor fusion
* Event-driven architecture
* Cloud-connected IoT system
* Scalable for multiple devices

---

## 📁 Project Structure

```id="b2v9sa"
HomeSecurityV2/
│
├── app.py
├── detection/
├── firebase/
├── static/
├── templates/
├── sensors/
└── requirements.txt
```

---

## 🔐 Use Cases

* Smart home security
* Intruder detection
* Fire and hazard monitoring
* IoT + AI system demonstrations

---

## 🔮 Future Improvements

* Multi-camera support
* Mobile notifications
* Edge processing optimization
* Dashboard analytics
* Deployment on cloud

---

## 👤 Author

**Raghuram Thiguti**
GitHub: [https://github.com/Turbid26](https://github.com/Turbid26)

---

* write a **1-line resume bullet (VERY important)**
* or optimize this for **recruiters scanning GitHub in 10 seconds**
