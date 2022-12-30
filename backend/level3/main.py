import json
from pathlib import Path
import datetime
import data_processing
import delivery_days_management
import oversea_management

input_file = Path("data/input.json")
test_input = json.loads(input_file.read_text())


def compute_deliveries(data: dict):
    deliveries = []
    promises_by_carriers = data_processing.promises_by_carriers(data)
    saturday_delivery_by_carriers = data_processing.saturday_delivery_by_carriers(data)
    oversea_delay_by_carriers = data_processing.oversea_delay_by_carriers(data)

    for package in data["packages"]:
        delivery_distance = data["country_distance"][package["origin_country"]][package["destination_country"]]
        original_delivery_promise = promises_by_carriers[package['carrier']]
        saturday_delivery = saturday_delivery_by_carriers[package['carrier']]
        oversea_delay_threshold = oversea_delay_by_carriers[package['carrier']]

        deliveries.append(delivery_info(delivery_distance, oversea_delay_threshold, package, original_delivery_promise,
                                        saturday_delivery))

    return {'deliveries': deliveries}


def delivery_info(delivery_distance, oversea_delay_threshold, package, original_delivery_promise,
                  saturday_delivery):
    """
    Processes the information for final estimation of the delivery
    :param delivery_distance:
    :param oversea_delay_threshold:
    :param package:
    :param original_delivery_promise:
    :param saturday_delivery:
    :return: dict with package_id, expected_delivery and oversea_delay
    """
    shipping_date = datetime.datetime.strptime(package['shipping_date'], '%Y-%m-%d')

    delivery_promise, oversea_delay = oversea_management.oversea_delivery_promise(original_delivery_promise,
                                                                                  oversea_delay_threshold,
                                                                                  delivery_distance)
    delivery_date = delivery_days_management.expected_delivery(shipping_date, delivery_promise, saturday_delivery)
    return {
        'package_id': package['id'],
        'expected_delivery': delivery_date.strftime('%Y-%m-%d'),
        'oversea_delay': oversea_delay
    }


if __name__ == '__main__':
    output = compute_deliveries(test_input)
    print(output)
