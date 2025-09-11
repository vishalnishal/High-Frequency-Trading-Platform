# High Frequency Trading Platform 🚀  

## 📌 Overview  
This project is a **low-latency High Frequency Trading (HFT) platform** that generates real-time **Buy, Sell, and Exit** signals for **NIFTY50**.  
It uses **Python (AI/ML, orchestration)** + **C++/Rust (low latency execution)** with a **Streamlit dashboard** for visualization.  

Key Features:  
- Real-time market data ingestion (NSEPython, Zerodha Kite API)  
- Technical indicators (EMA, RSI, MACD, Order Book analytics)  
- Confidence scoring for trading signals  
- Event-driven backend engine  
- Streamlit dashboard with OHLC charts & strategy selection  

---

## ⚙️ Project Structure  
```
hft_project/
│── backend/
│   ├── engine.py          # Core signal generation engine
│   ├── strategy.py        # Multiple trading strategies
│   └── utils.py           # Helper functions
│
│── frontend/
│   └── dashboard.py       # Streamlit dashboard (charts + strategy selection)
│
│── requirements.txt       # Python dependencies
│── README.md              # Project guide
│── venv/                  # Virtual environment (ignored in Git)
```

---

## 🔧 Installation & Setup  

### 1. Clone the Repository  
```bash
git clone https://github.com/your-username/hft_project.git
cd hft_project
```

### 2. Create a Virtual Environment  
```bash
python -m venv venv
```

### 3. Activate the Environment  
- **Windows (PowerShell)**  
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  ```  
- **Windows (CMD)**  
  ```cmd
  venv\Scripts\activate.bat
  ```  
- **Mac/Linux**  
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies  
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project  

### Run the Backend Engine (signal generator)  
```bash
python backend/engine.py
```

### Run the Frontend Dashboard (Streamlit UI)  
```bash
streamlit run frontend/dashboard.py
```

Dashboard will open at: [http://localhost:8501](http://localhost:8501)  

---

## 🛠 Troubleshooting  

- **Error: "scripts disabled" in PowerShell"**  
  Run:  
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

- **Streamlit not found**  
  Install manually:  
  ```bash
  pip install streamlit
  ```

- **Dashboard not updating with signals**  
  Ensure `engine.py` is running in one terminal and `dashboard.py` in another.  

---

## 👨‍💻 Team Members  
- Vishal (22BAI71398)  
- Harsh Kumar (22BAI71372)  

Supervisor: Aaskaran Bishnoi (E15060)  

---

## 📜 License  
This project is developed as part of **Capstone Project**. Patent filing in progress.  
