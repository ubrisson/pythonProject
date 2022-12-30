def promises_by_carriers(data):
    return {
        carrier["code"]: carrier["delivery_promise"]
        for carrier in data["carriers"]
    }


def saturday_delivery_by_carriers(data):
    return {
        carrier["code"]: carrier["saturday_deliveries"]
        for carrier in data["carriers"]
    }


def oversea_delay_by_carriers(data):
    return {
        carrier["code"]: carrier["oversea_delay_threshold"]
        for carrier in data["carriers"]
    }