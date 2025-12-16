# AI Agent Hybrid RAG: Enterprise Data Analyst

โปรเจกต์นี้เป็นระบบ **Hybrid Retrieval-Augmented Generation (Hybrid RAG)** สำหรับ **วิเคราะห์ข้อมูลองค์กร**
จุดเด่นคือความสามารถในการผสานข้อมูล 2 รูปแบบเข้าด้วยกัน:
1. **Structured Data:** ข้อมูลยอดขายและธุรกรรม (Transaction) ผ่าน **SQL Database**
2. **Unstructured Data:** ความคิดเห็นและ Feedback ลูกค้า ผ่าน **Vector Database**

ระบบใช้ **AI Router (LangGraph)** ในการตัดสินใจเลือกแหล่งข้อมูลอัตโนมัติ ทำให้สามารถตอบคำถามที่ซับซ้อน เช่น *"ยอดขายสินค้า A เป็นอย่างไร และลูกค้าบ่นเรื่องอะไรบ้าง?"* ได้อย่างแม่นยำ

---

## ฟีเจอร์หลัก (Features)
* **Intelligent Routing:** ใช้ `LangGraph` เป็นสมองกล ตัดสินใจว่าคำถามควรดึงข้อมูลจาก SQL, Vector หรือใช้ทั้งคู่
* **SQL Agent:** แปลงคำถามภาษาธรรมชาติเป็น SQL Query เพื่อหาผลรวม, ค่าเฉลี่ย, หรือสถิติยอดขาย
* **Semantic Search:** ค้นหา Insight จากรีวิวลูกค้าด้วย Vector Embeddings ไม่ใช่แค่ Keyword matching
---

## Tech Stack
* **Core:** Python, LangChain, LangGraph
* **Model:** OpenAI gpt-4.1-mini (สามารถปรับเปลี่ยนได้)
* **Database:**
  * **Structured:** SQLite
  * **Unstructured:** ChromaDB
* **Interface:** Streamlit

---

## โครงสร้างโปรเจกต์ (Structure)
```text
├── data/                 # ไฟล์ข้อมูลดิบ (CSV)
│   ├── sales_data.csv
│   └── customer_reviews.csv
├── setup_data/           # สคริปต์สำหรับ ETL ข้อมูลเข้า Database
│   ├── sql.py            # สร้าง SQLite DB จาก CSV
│   └── vector.py         # สร้าง Embeddings ลง ChromaDB
├── src/                  # Source code หลักของระบบ
│   ├── database.py       # การเชื่อมต่อ DB และโหลด Model
│   └── graph.py          # Logic ของ LangGraph (Router & Nodes)
├── app.py                # ไฟล์หลักสำหรับรัน Streamlit UI
└── requirements.txt
```

---

## การติดตั้งและใช้งาน (Installation & Usage)
1. Clone & Setup Environment:
```bash
git clone https://github.com/wiriyabot/AI-Agent-Hybrid-RAG.git
cd AI-Agent-Hybrid-RAG
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

---

2. Configuration
สร้างไฟล์ .env ที่ root folder และใส่ API Key:
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

3. Build Database
รันคำสั่งเพื่อแปลงไฟล์ CSV ในโฟลเดอร์ data/ ให้เป็น Database ที่พร้อมใช้งาน
```bash
# สร้าง SQL Database (sales.db)
python -m setup_data.sql

# สร้าง Vector Database (chroma_db)
python -m setup_data.vector
```

---

4. Run Application
```bash
streamlit run app.py
```

---

## หมายเหตุ
* สามารถเปลี่ยนข้อมูลในโฟลเดอร์ data/ เป็นไฟล์ CSV ของคุณเองได้ 

---

## ตัวอย่างการใช้งาน
การถามยอดขาย
<img width="2217" height="1187" alt="image" src="https://github.com/user-attachments/assets/58134b16-8db1-482b-a255-810f660a2766" />
การถามความคิดเห็น
<img width="2218" height="1185" alt="image" src="https://github.com/user-attachments/assets/725cfc28-d6a9-4e53-b12c-872b588c6c36" />
คำถามผสม
<img width="927" height="1062" alt="image" src="https://github.com/user-attachments/assets/0e32612d-431c-43af-9a8a-395a0d1809d7" />


