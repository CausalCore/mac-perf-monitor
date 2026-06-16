def calculate_trend(values):
    """
    Calculates the slope (trend) of a list of numeric values.
    Returns >0 for upward trend, <0 for downward.
    """
    if len(values) < 2:
        return 0.0

    # Simple linear regression slope
    n = len(values)
    sum_x = sum(range(n))
    sum_y = sum(values)
    sum_x2 = sum(x * x for x in range(n))
    sum_xy = sum(x * y for x, y in enumerate(values))

    denominator = n * sum_x2 - sum_x * sum_x
    if denominator == 0:
        return 0.0

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    return slope
