from datetime import datetime, timedelta

def calculate_dynamic_price(
    base_fare,
    available_seats,
    total_seats,
    departure_time,
    demand_level,
    pricing_tier
):
    """
    Dynamic pricing formula:
    base_fare * (1 + seat + time + demand + tier)
    """

    # --------------------------------------------------
    # 1️⃣ Normalize departure_time (CRITICAL FIX)
    # --------------------------------------------------
    if isinstance(departure_time, str):
        departure_time = departure_time.strip()

        # Try common time formats
        for fmt in ("%I:%M %p", "%H:%M"):
            try:
                parsed_time = datetime.strptime(departure_time, fmt)
                break
            except ValueError:
                parsed_time = None

        if parsed_time is None:
            # Fallback: assume flight is far in future
            parsed_time = datetime.utcnow() + timedelta(hours=72)

        # Attach today's date so datetime math works
        now = datetime.utcnow()
        departure_time = parsed_time.replace(
            year=now.year,
            month=now.month,
            day=now.day
        )

    # --------------------------------------------------
    # 2️⃣ Seat factor (scarcity-based)
    # --------------------------------------------------
    seat_ratio = available_seats / total_seats
    seat_factor = (1 - seat_ratio) * 0.5   # up to +50%

    # --------------------------------------------------
    # 3️⃣ Time factor (urgency-based)
    # --------------------------------------------------
    hours_left = max(
        (departure_time - datetime.utcnow()).total_seconds() / 3600,
        0
    )

    if hours_left > 72:
        time_factor = 0.0
    elif hours_left > 24:
        time_factor = 0.15
    else:
        time_factor = 0.35

    # --------------------------------------------------
    # 4️⃣ Demand factor
    # --------------------------------------------------
    demand_factor = {
        "low": 0.05,
        "medium": 0.15,
        "high": 0.30
    }.get(demand_level, 0.15)

    # --------------------------------------------------
    # 5️⃣ Pricing tier factor
    # --------------------------------------------------
    tier_factor = {
        "economy": 0.0,
        "premium": 0.25,
        "business": 0.6
    }.get(pricing_tier, 0.0)

    # --------------------------------------------------
    # 6️⃣ Final dynamic price
    # --------------------------------------------------
    dynamic_price = base_fare * (
        1 + seat_factor + time_factor + demand_factor + tier_factor
    )

    return round(dynamic_price)
