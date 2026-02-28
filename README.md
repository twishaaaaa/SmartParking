# 🚗 Smart Campus Parking System

> A full-stack, cloud-integrated parking management solution developed for **SCET Surat**.  
> Digitizes vehicle entry/exit using QR Code technology with real-time occupancy tracking for **3,000+ daily vehicles**.

---

## 🌟 Key Features

- **☁️ Cloud Database** — Real-time data persistence using MongoDB Atlas
- **📲 QR-Based Authentication** — Automated generation of unique QR stickers for student vehicles
- **🎯 Security Guard Interface** — Integrated camera scanner with instant audio and visual feedback
- **🔢 Categorized Capacity** — Separate tracking and limits for 2-Wheeler (2,000 slots) and 4-Wheeler (1,000 slots) zones
- **📊 Admin Dashboard** — Live occupancy progress bars, owner lookup by plate number, and a recent activity log with timestamps

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / Flask |
| Database | MongoDB Atlas (NoSQL) |
| Frontend | HTML5, Bootstrap 5, JavaScript |
| QR Scanning | html5-qrcode |
| QR Generation | qrcode |
| DB Connection | PyMongo |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- A MongoDB Atlas account and connection string

### 1. Clone & Install

```bash
git clone https://github.com/your-username/smart-campus-parking.git
cd smart-campus-parking
pip install -r requirements.txt
```

### 2. Configure MongoDB

Open `app.py` and replace the placeholder with your Atlas connection string:

```python
app.config["MONGO_URI"] = "mongodb+srv://your_username:password@cluster0..."
```

### 3. Run the Server

```bash
python app.py
```

Visit the dashboard at **http://127.0.0.1:5000**

---

## 📂 Project Structure

```
SmartParking/
├── app.py                  # Flask backend & MongoDB logic
├── requirements.txt        # Project dependencies
├── static/
│   ├── qrcodes/            # Generated QR code images
│   ├── success.mp3         # Audio for approved entry
│   └── error.mp3           # Audio for denied entry
└── templates/
    └── index.html          # Dashboard & scanner UI
```

---

## 📊 System Logic

```
[Registration] ──► [Scan QR] ──► [Validate ID & Zone Capacity] ──► [Log IN/OUT + Timestamp]
```

1. **Registration** — Student details saved to MongoDB Atlas; unique ID and QR code generated
2. **Scanning** — Security guard scans the QR code via the camera interface
3. **Validation** — System verifies the ID in MongoDB and checks if the zone (2W/4W) has available space
4. **Logging** — Status flips between IN/OUT and a timestamp is recorded in the Admin activity log

---

## 👨‍💻 Developer

**Twisha Savani**  
IT Student, SCET Surat
