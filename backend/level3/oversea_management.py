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