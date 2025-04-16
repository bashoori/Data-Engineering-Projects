# 🏥 Healthcare FHIR Data Pipeline (Demo Project)

This project simulates a real-world healthcare data pipeline using **FHIR-formatted** patient records and modern data engineering tools. It demonstrates how to ingest, normalize, model, and visualize clinical data in a structured, scalable way.

---

## 🧬 What is FHIR?

FHIR (Fast Healthcare Interoperability Resources) is a widely adopted standard for formatting and exchanging healthcare data. It defines how key patient information — such as demographics, medical encounters, observations (like lab results), and conditions — should be structured and shared between systems.

This project processes structured FHIR JSON files (generated via Synthea or public examples) and converts them into clean, relational tables that are analytics-ready.

🔗 Learn more: [https://www.hl7.org/fhir/overview.html](https://www.hl7.org/fhir/overview.html)

---

## 📦 Project Features

✅ Ingest FHIR JSON resources (e.g. `Patient`, `Observation`, `Encounter`)  
✅ Normalize nested healthcare data into flat relational tables  
✅ Load structured data into BigQuery or SQLite  
✅ (Optional) Orchestrate with Airflow and visualize with Looker Studio or Streamlit  
✅ Emulates data use cases in healthcare analytics & ML workflows

---

## 🧰 Tech Stack

- **Languages:** Python, SQL  
- **Standards:** FHIR (Patient, Observation, Encounter schemas)  
- **Cloud:** Google Cloud Platform (BigQuery, Cloud Storage, Cloud Functions)  
- **Tools:** Pandas, Airflow (local), Looker Studio / Streamlit  
- **Optional:** GitHub Actions for CI/CD automation

---

## 🗂 Folder Structure

```
healthcare-fhir-data-pipeline/
├── data/                # FHIR JSON files
├── scripts/             # Python scripts for parsing and transformation
├── pipeline/            # ETL logic, DAGs, DB loading
├── notebooks/           # Optional: analysis or testing
├── dashboard/           # Visualization templates
├── requirements.txt     # Python dependencies
└── README.md            # Project overview
```

---

## 🗺️ FHIR Data Pipeline Flow

![FHIR Pipeline](FHIR_Data_Pipeline_Diagram.png)

---

## 🚀 How to Run

1. Clone the repo and navigate into it  
2. Install dependencies:  
   ```
   pip install -r requirements.txt
   ```
3. Place FHIR `.json` files into `/data`  
4. Run the parser script:  
   ```
   python scripts/fhir_parser.py
   ```
5. (Optional) Load output to BigQuery or SQLite using `pipeline/load_to_bq.py`  
6. (Optional) Visualize insights with Looker or Streamlit

---

## 📈 Example Dashboard Ideas

- Patient count by gender and age group  
- Most common conditions (e.g. diabetes, hypertension)  
- Trends in encounter types or medication usage  
- Observations (e.g. lab values) by category

---

## 🤝 Let's Collaborate

This project is part of my [data engineering portfolio](https://github.com/bashoori).  
Feel free to fork, contribute, or suggest improvements!

