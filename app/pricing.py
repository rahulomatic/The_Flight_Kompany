# app/pricing.py
from datetime import datetime, timedelta
import math
import random

def _seat_factor(seats_available: int, seats_total: int) -> float:
    """Higher factor as seats left decrease. Returns a value like 0.0..0.6"""
    if seats_total <= 0:
        return 0.0
    pct = seats_available / seats_total  # 1.0 = full, 0.0 = sold out
    # Example: if pct=0.1 (10% left) -> multiplier contribution = 0.45
    # Use a curve so price grows faster as pct->0
    return max(0.0, (1 - pct) ** 1.5) * 0.6   # tuned constants, change as needed

def _time_factor(departure: datetime, now: datetime = None) -> float:
    """Returns factor based on time until departure. Closer -> larger factor."""
    now = now or datetime.utcnow()
    delta = departure - now
    days = max(delta.total_seconds(), 0) / 86400.0  # days until departure
    # If >30 days away -> low factor; if <1 day -> high factor
    if days >= 30:
        return 0.0
    if days <= 1:
        return 0.5  # strong urgency
    # Smooth curve between 30 and 1 days
    return max(0.0, (1 / days) * 0.25)  # tuned constant

def _demand_factor(simulated_demand_index: float) -> float:
    """Demand index expected between 0.0 (low) and 1.0 (high)."""
    return (simulated_demand_index - 0.5) * 0.6  # maps 0..1 to -0.3..+0.3

def _tier_factor(tier: str) -> float:
    """Airline pricing tier: 'economy', 'standard', 'premium' - tuned multipliers"""
    mapping = {
        "economy": 0.0,
        "standard": 0.05,
        "premium": 0.12,
    }
    return mapping.get((tier or "").lower(), 0.0)

def calculate_dynamic_price(
    base_fare: float,
    seats_available: int,
    seats_total: int,
    departure: datetime,
    simulated_demand_index: float = 0.5,
    airline_tier: str | None = None,
    now: datetime | None = None,
) -> float:
    """
    Returns new dynamic price (float).
    - base_fare: base price stored in DB
    - seats_available / seats_total: inventory
    - departure: datetime (UTC ideally)
    - simulated_demand_index: float 0..1 (0 low demand, 1 high demand)
    - airline_tier: optional pricing tier string
    """
    now = now or datetime.utcnow()
    # guard rails
    seats_total = max(seats_total or 0, 0)
    seats_available = max(seats_available or 0, 0)
    base_fare = max(float(base_fare or 0.0), 0.0)

    seat = _seat_factor(seats_available, seats_total)
    timef = _time_factor(departure, now)
    demand = _demand_factor(simulated_demand_index)
    tier = _tier_factor(airline_tier)

    total_factor = seat + timef + demand + tier

    # add a small randomization to mimic micro fluctuations
    rand_noise = random.uniform(-0.02, 0.03)  # -2% .. +3%
    total_factor = total_factor + rand_noise

    # final price: ensure not below a floor (e.g., 50% of base) and not negative
    new_price = base_fare * (1 + total_factor)
    floor = max(0.5 * base_fare, 50.0)  # don't drop below 50% base or a minimum absolute floor
    new_price = max(new_price, floor)

    # round to 2 decimals
    return round(new_price, 2)