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

# Carriers add one day on their delivery promise for every [oversea delay] kms separating the origin and delivery country. Oversea delay varies by carrier.
#
# e.g. Colissimo normally ships in 3 business days, but a package from France to Japan will be delivered in 6 business days since Japan is 9500km away from France and Colissimo distance threshold is 3000km
#
# Compute the new expected deliveries taking that extended delay into account. Week ends should still be accounted for. The result should include the oversea delay length in days.


import json
from pathlib import Path
import datetime

input_file = Path("data/input.json")
test_input = json.loads(input_file.read_text())

output_file = Path("data/expected_output.json")
expected_output = json.loads(output_file.read_text())


def oversea_delivery_promise(delivery_promise, oversea_delay_threshold, distance):
    """
    Carriers add one day on their delivery promise
    for every [oversea delay] kms separating the origin and delivery country.
    Oversea delay varies by carrier.
    :return: a delivery promise in days and the associated delay
    """
    delay = 0
    if distance > oversea_delay_threshold:
        delay = (distance - 1) // oversea_delay_threshold
        delivery_promise += delay
    return delivery_promise, delay


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
    oversea_delay_by_carriers = {
        carrier["code"]: carrier["oversea_delay_threshold"]
        for carrier in data["carriers"]
    }

    for package in data["packages"]:
        shipping_date = datetime.datetime.strptime(package['shipping_date'], '%Y-%m-%d')

        original_delivery_promise = promises_by_carriers[package['carrier']]
        distance = data["country_distance"][package["origin_country"]][package["destination_country"]]
        oversea_delay_threshold = oversea_delay_by_carriers[package['carrier']]
        delivery_promise, oversea_delay = oversea_delivery_promise(original_delivery_promise, oversea_delay_threshold,
                                                                   distance)

        delivery_date = expected_delivery(shipping_date, delivery_promise,
                                          saturday_delivery_by_carriers[package['carrier']])
        deliveries.append({
            'package_id': package['id'],
            'expected_delivery': delivery_date.strftime('%Y-%m-%d'),
            'oversea_delay': oversea_delay
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
