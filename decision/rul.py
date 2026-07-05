def estimate_rul(health):

    if health <= 0:
        return 0

    return int(health * 250)