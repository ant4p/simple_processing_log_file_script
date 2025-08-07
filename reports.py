import json
from datetime import datetime
from collections import defaultdict

from utils import get_files_list, get_search_dates



def average_report(file, date=None):
    file_list = get_files_list(file)

    stats = defaultdict(lambda: {"total": 0, "avg_response_time": 0.0})

    filter_date = get_search_dates(date)

    try:
        for item in file_list:
            with open(item, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())

                        if filter_date is not None:
                            log_time = datetime.strptime(log_entry['@timestamp'], '%Y-%m-%dT%H:%M:%S%z')
                            if log_time.date() not in filter_date:
                                continue

                        handler = log_entry.get("url", "")
                        if not handler:
                            continue

                        response_time = float(log_entry.get("response_time", 0.0))

                        key = f"{handler}"
                        stats[key]["total"] += 1
                        stats[key]["avg_response_time"] += response_time

                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"Ошибка {e}")
    except FileNotFoundError:
        print(f"Файл {file} не найден.")

    return stats
