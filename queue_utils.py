import os
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
import sqlite3

DATA_DIR = "data"
DB_FILE = "queue_data.db"
os.makedirs(DATA_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interconnection_queue_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iso_name TEXT,
            queue_id TEXT,
            project_name TEXT,
            location TEXT,
            status TEXT,
            fuel_type TEXT,
            capacity_mw REAL,
            requested_in_service_date DATE,
            application_date DATE,
            developer_name TEXT,
            interconnection_voltage_kv TEXT,
            notes TEXT,
            last_updated TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_to_db(df):
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("interconnection_queue_projects", conn, if_exists="append", index=False)
    conn.close()

def fetch_xls(url, iso):
    response = requests.get(url)
    xls = pd.ExcelFile(BytesIO(response.content))
    df = xls.parse(xls.sheet_names[0])
    df['ISO'] = iso
    return df

def normalize(df):
    df_norm = pd.DataFrame()
    df_norm['iso_name'] = df['ISO']
    df_norm['queue_id'] = df.get('Queue Number', df.get('GI Queue #', df.get('Queue ID', '')))
    df_norm['project_name'] = df.get('Project Name', df.get('Project', ''))
    df_norm['location'] = df.get('County', df.get('Location', ''))
    df_norm['status'] = df.get('Status', '')
    df_norm['fuel_type'] = df.get('Fuel Type', df.get('Fuel', ''))
    df_norm['capacity_mw'] = df.get('MW', df.get('Capacity (MW)', 0))
    df_norm['requested_in_service_date'] = pd.to_datetime(df.get('In-Service Date', df.get('Target COD', pd.NaT)), errors='coerce')
    df_norm['application_date'] = pd.to_datetime(df.get('Queue Date', pd.NaT), errors='coerce')
    df_norm['developer_name'] = df.get('Interconnection Customer', df.get('Developer', ''))
    df_norm['interconnection_voltage_kv'] = df.get('Voltage Level', '')
    df_norm['notes'] = ''
    df_norm['last_updated'] = pd.Timestamp.now()
    return df_norm

ISO_URLS = {
    "PJM": 'https://www.pjm.com/-/media/planning/gen-queue/queue-position.ashx',
    "MISO": 'https://www.misoenergy.org/media/377845/GIQ_Table.xlsx',
    "CAISO": 'https://www.caiso.com/Documents/ISOGeneratorInterconnectionQueue.xlsx',
    "NYISO": 'https://www.nyiso.com/documents/20142/1402339/NYISO-Interconnection-Queue.xlsx',
    "ISO-NE": 'https://www.iso-ne.com/static-assets/documents/2024/03/qtp_interconnection_requests.xlsx',
    "ERCOT": 'https://www.ercot.com/files/docs/2024/03/25/Monthly_Generation_Interconnection_Status.xlsx',
    "SPP": 'https://spp.org/documents/queue.xlsx'
}
