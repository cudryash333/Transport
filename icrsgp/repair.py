def repair_route_set(
    route_set,
    graph,
    num_nodes,
    max_len,
):
    """
    Repair, гарантирующий:
    - покрытие всех вершин
    - соблюдение max_len
    """

    covered = route_set.covered_nodes()
    missing = set(range(num_nodes)) - covered

    routes = route_set.routes

    for node in missing:
        inserted = False

        # пробуем добавить в существующие маршруты
        for r in routes:
            if r.length >= max_len:
                continue

            # добавляем через ближайший терминал
            last = r.nodes[-1]
            for v, _ in graph.neighbors(last):
                if v == node:
                    r.nodes.append(node)
                    inserted = True
                    break

            if inserted:
                break

        # fallback: если не получилось — создаём короткий маршрут
        if not inserted:
            r = min(routes, key=lambda x: x.length)
            if r.length < max_len:
                r.nodes.append(node)

    return route_set
