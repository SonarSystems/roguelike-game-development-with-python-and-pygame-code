def amount_for_depth(rows, depth):
    amount = 0
    for start_depth, value in rows:
        if start_depth <= depth:
            amount = value
    return amount
