import heapq


def shortest_path(edges, source, destination):
    graph = {}

    for edge in edges:
        graph.setdefault(edge.source, []).append(
            (edge.destination, edge.latency)
        )

    pq = [(0, source, [])]

    visited = set()

    while pq:
        total_latency, current_node, path = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        path = path + [current_node]

        if current_node == destination:
            return total_latency, path

        for neighbor, weight in graph.get(current_node, []):
            heapq.heappush(
                pq,
                (total_latency + weight, neighbor, path)
            )

    return None, None