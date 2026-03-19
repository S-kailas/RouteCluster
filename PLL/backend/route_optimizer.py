def nearest_neighbor(matrix, start_index=0, end_index=None):

    n = len(matrix)

    if n == 0:
        return []

    visited = [False] * n
    order = [start_index]
    visited[start_index] = True

    for _ in range(n - 1):

        last = order[-1]
        next_idx = None
        min_dist = float("inf")

        for i in range(n):
            if not visited[i] and matrix[last][i] < min_dist:
                min_dist = matrix[last][i]
                next_idx = i

        order.append(next_idx)
        visited[next_idx] = True

    # If end point is defined → force it to last
    if end_index is not None and end_index in order:
        order.remove(end_index)
        order.append(end_index)

    return order
