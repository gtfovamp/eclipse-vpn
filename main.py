from fastapi import FastAPI
import httpx
import csv
from io import StringIO
import uvicorn  

app = FastAPI()

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

@app.get("/vpn-data/")
async def get_vpn_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.vpngate.net/api/iphone/")
        csv_data = response.text
        
        reader = csv.reader(StringIO(csv_data.strip()))
        rows = list(reader)
        
        vpn_list = []
        for row in rows[2:-1]:  # Пропускаем первые 2 строки и последнюю
            if not row or len(row) < 15 or row[0].startswith('*'):
                continue
            
            vpn_list.append({
                "host": row[0],
                "ip": row[1],
                "score": safe_int(row[2]),
                "ping": safe_int(row[3]),
                "speed": safe_int(row[4]),
                "country": row[5],
                "sessions": safe_int(row[6]),
                "uptime": safe_int(row[7]),
                "total_users": safe_int(row[8]),
                "total_traffic": safe_int(row[9]),
                "config": row[14] if len(row) > 14 else ""
            })
        
        return vpn_list
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)