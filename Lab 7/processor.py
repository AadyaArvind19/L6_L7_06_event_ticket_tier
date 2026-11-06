
def decode_promo_voucher(voucher_code):
    if not isinstance(voucher_code, str):
        return "Invalid voucher code"

    code = voucher_code.strip()
    parts = code.split("-")

    if len(parts) != 2:
        return "Invalid voucher code"

    prefix, pct_str = parts
    prefix = prefix.strip().upper()

    if not prefix or not pct_str.isdecimal():
        return "Invalid voucher code"

    percentage = int(pct_str)

    if percentage < 0 or percentage > 100:
        return "Invalid voucher code"

    return f"Valid {prefix}: {percentage}% OFF"


def calculate_seat_tier_price(tier_spec):
    if not isinstance(tier_spec, str):
        return "Invalid tier specification"

    parts = tier_spec.split("@")

    if len(parts) != 2:
        return "Invalid tier specification"

    tier = parts[0].strip().upper()

    tier_rates = {
        "VIP": 150.0,
        "PREMIUM": 90.0,
        "GENERAL": 45.0
    }

    if tier not in tier_rates:
        return "Invalid tier specification"

    try:
        row = int(parts[1])
    except (ValueError, OverflowError):
        return "Invalid tier specification"

    if row < 1:
        return "Invalid tier specification"

    base = tier_rates[tier]
    return base + (row * 2.0)


def parse_attendee_badge(badge_csv):
    if not isinstance(badge_csv, str):
        return "Invalid attendee badge"

    tokens = badge_csv.split(",")

    if len(tokens) != 3:
        return "Invalid attendee badge"

    name = tokens[0].strip()
    age_str = tokens[1].strip()
    seat = tokens[2].strip()

    if not name or not seat or not age_str.isdecimal():
        return "Invalid attendee badge"

    try:
        age = int(age_str)
    except (ValueError, OverflowError):
        return "Invalid attendee badge"

    if age < 0 or age > 120:
        return "Invalid attendee badge"

    category = "Child" if age < 18 else "Adult"

    return f"{name} [{category}] - Seat {seat}"


def main():
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    print("Voucher:", decode_promo_voucher(v_input))

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    print("Seat Price: $", calculate_seat_tier_price(t_input))

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    print("Badge:", parse_attendee_badge(b_input))


if __name__ == "__main__":
    main()
