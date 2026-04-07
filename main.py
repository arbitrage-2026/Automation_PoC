from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg2
from rca_engine import analyze_root_cause

app = FastAPI()

conn = psycopg2.connect(os.getenv("DB_URL"))

class DeviceData(BaseModel):
    tenant_id: str
    device_name: str
    cpu: float
    memory: float
    disk: float

@app.post("/heartbeat")
def heartbeat(data: DeviceData):
    cur = conn.cursor()

    # Insert telemetry
    cur.execute("""
        INSERT INTO telemetry (tenant_id, cpu, memory, disk)
        VALUES (%s, %s, %s, %s)
    """, (data.tenant_id, data.cpu, data.memory, data.disk))

    # Basic RCA Trigger
    if data.cpu > 85 or data.disk < 10:
        result = analyze_root_cause(data.dict())
        action = result.get("action")

        cur.execute("""
            INSERT INTO actions (action, status)
            VALUES (%s, %s)
        """, (action, "triggered"))

        conn.commit()
        return {"action": action, "rca": result}

    conn.commit()
    return {"status": "ok"}