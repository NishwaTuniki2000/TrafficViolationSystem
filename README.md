# 🚦 Traffic Violation Detection System

The **Traffic Violation Detection System** is a full-stack application that detects and records traffic violations in real time using computer vision, deep learning, and modern web technologies.  
It integrates a **Python FastAPI backend (deployed on Render)** with a **React frontend (deployed on Vercel)** to provide a complete monitoring and reporting solution.

---

## 🖥️ Backend (FastAPI + AI Models)

**Frameworks**: FastAPI, Uvicorn  

**ML/AI Components**:
- **YOLOv8 (Ultralytics)** – detects vehicles, traffic lights, and number plates.  
- **DeepSORT** – tracks vehicles across video frames.  
- **EasyOCR** – extracts text from license plates.  

**Features**:
- Detects violations such as:  
  - 🚨 Running a red light  
  - 🚗 Overspeeding (via rule-based speed checks)  
  - 🛣️ Lane violations  
- Stores snapshots of violations (images & metadata).  
- Provides **REST APIs** and **WebSocket** for live video streaming.  

**Deployment**: Hosted on **Render** with a public API:
- API Docs → `/docs`  
- Live WebSocket → `/live-video`  

---

## 🌐 Frontend (React + Vercel)

**Frameworks**: React.js, WebSocket API, Fetch API  

**Features**:
- Real-time **video monitoring interface**.  
- **Violation reports dashboard** (images + license plate numbers).  
- REST integration with backend APIs.  
- WebSocket for **live traffic feed visualization**.  

**Deployment**: Hosted on **Vercel** with CI/CD from GitHub.  



