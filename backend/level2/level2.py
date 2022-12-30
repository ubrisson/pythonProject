# Each shipping carrier has specific delivery promises (in days).
# The online retailers assigns a shipping date and a carrier to each order.
#
# We first want to compute a list of expected delivery dates for some packages.
# Level 2

# - Carriers will not work on Sundays.
# - Some carriers will work on Saturdays while some others won't.
# - When a carrier isn't working, package deliveries will not make any progress on that day. The delivery will thus be postponed by 1 day.
#
# Adapt the expected delivery computation to take these new rules into account.


import json
from pathlib import Path
import datetime

input_file = Path("data/input.json")
test_input = json.loads(input_file.read_text())

output_file = Path("data/expected_output.json")
expected_output = json.loads(output_file.read_text())


def compute_deliveries(data: dict):
    deliveries = []
    promises_by_carriers = {
        carrier["code"]: carrier["delivery_promise"]
        for carrier in data["carriers"]
    }
    saturday_delivery_by_carriers = {
        carrier["code"]: carrier["saturday_deliveries"]
        for carrier in data["carriers"]
    }

    for package in data["packages"]:
        shipping_date = datetime.datetime.strptime(package['shipping_date'], '%Y-%m-%d')
        delivery_promise = promises_by_carriers[package['carrier']]
        delivery = expected_delivery(shipping_date, delivery_promise, saturday_delivery_by_carriers[package['carrier']])
        deliveries.append({
            'package_id': package['id'],
            'expected_delivery': delivery.strftime('%Y-%m-%d')
        })
    return {'deliveries': deliveries}


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


if __name__ == '__main__':
    test_output = compute_deliveries(test_input)
    print(test_output)

    # print(expected_output)
    # print(test_output == expected_output)
