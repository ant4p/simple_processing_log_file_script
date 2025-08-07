import os

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


DEFAULT_DIRECTORY = os.getenv("DEFAULT_DIRECTORY")


# Получаем список файлов для обработки
def get_files_list(file):
    files_list = [os.path.join(DEFAULT_DIRECTORY, path) for path in file]
    return files_list

# Получаем список дат для обработки
def get_search_dates(date_input=None):
    if date_input is None:
        return None
    if date_input is not None:
        try:
            date_list = [date_input] if isinstance(date_input, str) or not hasattr(date_input, '__iter__') else date_input
            print()
            dates_filtered_list = []
            for dates in date_list:
                date_str = str(dates) if not isinstance(dates, str) else dates
                filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                dates_filtered_list.append(filter_date)
            return dates_filtered_list
        except ValueError:
            print(f"Неверный формат даты: {date_input}. Введите дату в формате YYYY-MM-DD")
            return {}
