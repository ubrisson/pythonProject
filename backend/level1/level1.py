# Each shipping carrier has specific delivery promises (in days).
# The online retailers assigns a shipping date and a carrier to each order.
#
# We first want to compute a list of expected delivery dates for some packages.


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
        carrier["code"]:  carrier["delivery_promise"]
        for carrier in data["carriers"]
    }

    for package in data["packages"]:
        shipping_date = datetime.datetime.strptime(package['shipping_date'], '%Y-%m-%d')
        delivery_promise = promises_by_carriers[package['carrier']]
        expected_delivery = shipping_date + datetime.timedelta(days=delivery_promise + 1)
        deliveries.append({
            'package_id': package['id'],
            'expected_delivery': expected_delivery.strftime('%Y-%m-%d')
        })
    return {'deliveries': deliveries}


if __name__ == '__main__':
    test_output = compute_deliveries(test_input)
    print(test_output)
    # print(test_output == expected_output)
