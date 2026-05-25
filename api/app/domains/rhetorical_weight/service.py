def apply_rhetorical_weight(average: float, weight: float | None) -> float:
    if weight is None or weight == 1.0:
        return average
    if weight <= 0:
        return 0.0
    sign = 1.0 if average > 0 else (-1.0 if average < 0 else 0.0)
    return sign * (abs(average) ** (1.0 / weight))
