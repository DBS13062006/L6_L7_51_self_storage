import math

GST_RATE = 1.18


def _to_finite_float(value):
    """Convert text to a finite float, or return None if that is not possible."""
    try:
        number = float(value.strip())
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(number):
        return None
    return number


def parse_rental(text):
    """Parse 'unit:months' into (Unit, months). Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    unit = parts[0].strip()
    if not unit:
        return None
    months = _to_finite_float(parts[1])
    if months is None or months <= 0:
        return None
    return unit.title(), months


def duration_average(months_csv):
    """Integer average of comma separated rental months. Returns None for invalid input."""
    if not isinstance(months_csv, str):
        return None
    values = []
    for raw in months_csv.split(','):
        raw = raw.strip()
        if not raw:
            return None
        try:
            months = int(raw)
        except ValueError:
            return None
        if months <= 0:
            return None
        values.append(months)
    if not values:
        return None
    return sum(values) // len(values)


def payable_rent(text):
    """Rent with 18% GST minus discount, never below zero. Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    rent = _to_finite_float(parts[0])
    discount = _to_finite_float(parts[1])
    if rent is None or discount is None or rent < 0 or discount < 0:
        return None
    total = rent * GST_RATE - discount
    if not math.isfinite(total):
        return None
    return round(max(total, 0.0), 2)


def _read(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def main():
    print("==== Running parse_rental ====")
    user_input = _read("Enter unit:months (e.g. medium:6): ")
    result = parse_rental(user_input)
    if result is None:
        print("Invalid input: expected unit:months with a positive number of months")
    else:
        print("Unit and Months:", result)

    print("\n==== Running duration_average ====")
    user_input = _read("Enter rental months as CSV (e.g. 3,6,12): ")
    result = duration_average(user_input)
    if result is None:
        print("Invalid input: expected positive whole numbers separated by commas")
    else:
        print("Average Duration:", result)

    print("\n==== Running payable_rent ====")
    user_input = _read("Enter rent|discount (e.g. 2400|200): ")
    result = payable_rent(user_input)
    if result is None:
        print("Invalid input: expected rent|discount with non-negative numbers")
    else:
        print("Payable Rent:", result)


if __name__ == "__main__":
    main()
