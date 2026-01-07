
from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/external_feed/sample")
def sample_feed(count: int = 20):
    airports = ["BLR","DEL","MAA","BOM","HYD","COK","CCU","AMD","GOI"]
    airlines = ["Indigo","AirIndia","Vistara","SpiceJet","GoAir"]
    now = datetime.utcnow()
    items = []
    for i in range(count):
        origin, destination = random.sample(airports, 2)
        dep = now + timedelta(days=random.randint(0,10), hours=random.randint(0,23))
        arr = dep + timedelta(hours=random.randint(1,5))
        items.append({
            "airline": random.choice(airlines),
            "flight_number": f"XX{random.randint(100,999)}",
            "origin": origin,
            "destination": destination,
            "departure": dep.isoformat(),
            "arrival": arr.isoformat(),
            "price": round(random.uniform(1000,12000), 2),
            "seats_total": random.choice([120, 150, 180]),
            "seats_available": random.randint(0, 180),
        })
    return {"feed_generated_at": now.isoformat(), "flights": items}
