# 🚀 ChatUTM - Installation Guide

## 📌 Backend Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/7azmi/chatutm.git
cd chatutm
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the FastAPI Server**
```bash
uvicorn app.main:app --reload
```

### **4️⃣ Test API Endpoints**
- Open **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Root endpoint: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📌 Frontend Setup

### **1️⃣ Open Directly in Browser**
- Open `frontend/index.html` in your browser.

### **2️⃣ Serve Locally (Optional)**
```bash
cd frontend
python3 -m http.server 8080
```
- Open: [http://localhost:8080](http://localhost:8080)

---

✅ **ChatUTM is ready to go!**

