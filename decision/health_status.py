def get_component_status(health):

    if health >= 90:
        return "Healthy"

    elif health >= 70:
        return "Warning"

    elif health >= 50:
        return "Service Required"

    else:
        return "Critical"