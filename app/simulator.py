# app/simulator.py
import asyncio
import random
from datetime import datetime
from typing import Dict

from .database import SessionLocal
from . import crud, models
from .pricing import calculate_dynamic_price

# In-memory demand index map {flight_id: float}
_demand_index: Dict[int, float] = {}

async def simulate_market_step():
    """
    One simulation step:
    - For a sample of flights, randomly change seats_available a little
    - Compute dynamic price and update DB + log pricing history
    """
    db = SessionLocal()
    try:
        flights = crud.get_all_flights_for_simulation(db)
        if not flights:
            return
        # pick a subset to update (to keep writes small)
        sample = random.sample(flights, k=min(len(flights), max(10, len(flights)//10)))
        now = datetime.utcnow()
        for f in sample:
            # initialize demand index if not present
            di = _demand_index.get(f.id, random.uniform(0.3, 0.7))
            # randomly nudge demand and clamp to 0..1
            di += random.uniform(-0.08, 0.12)
            di = max(0.0, min(1.0, di))
            _demand_index[f.id] = di

            # randomly change seats_available by -2 .. +3 (simulate bookings/cancellations)
            change = random.randint(-3, 3)
            new_available = max(0, min(f.seats_total, f.seats_available + change))

            # If seats actually changed, assign and persist
            if new_available != f.seats_available:
                f.seats_available = new_available

            # compute new dynamic price
            new_price = calculate_dynamic_price(
                base_fare=f.price,  # if you store base_fare separate, use that
                seats_available=f.seats_available,
                seats_total=f.seats_total,
                departure=f.departure,
                simulated_demand_index=di,
                airline_tier=getattr(f, "airline_tier", None),
                now=now
            )

            # update flight price and log history
            reason = f"sim-step demand={di:.2f} seats={f.seats_available}"
            crud.update_flight_price(db, f, new_price, reason=reason)
        # done
    except Exception as e:
        db.rollback()
        print("Simulator error:", e)
    finally:
        db.close()

async def scheduler_loop(interval_seconds: int = 60):
    """
    Continuously run the market simulation every `interval_seconds`.
    Use small intervals for dev (60s). For production this would be a worker.
    """
    while True:
        await simulate_market_step()
        await asyncio.sleep(interval_seconds)