import datetime


def expected_delivery(shipping_date, delivery_promise, carrier_saturday_deliveries):
    current_date = shipping_date
    delivery_days = 0
    while delivery_days <= delivery_promise:
        current_date += datetime.timedelta(days=1)
        # Sunday
        if current_date.weekday() == 6:
            continue
        # Saturday
        elif current_date.weekday() == 5 and not carrier_saturday_deliveries:
            continue
        # Open day for delivery
        else:
            delivery_days += 1

    return current_date
