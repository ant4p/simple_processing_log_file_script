import tabulate


def average_tabulate(stats):
    table_data = []

    for handler, stats in stats.items():
        table_data.append(
            [handler, stats["total"], f"{stats['avg_response_time']:.3f}"]
        )

    table_data.sort(key=lambda x: x[2], reverse=True)

    headers = ["handler", "total", "avg_response_time"]
    result = tabulate.tabulate(
        table_data,
        headers=headers,
        showindex=range(0, len(table_data)),
        tablefmt="simple",
    )

    return result
