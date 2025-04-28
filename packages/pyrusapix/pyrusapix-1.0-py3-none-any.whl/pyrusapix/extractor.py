import aiohttp
import json
from typing import Optional, List, Dict, Union, Any
from .exceptions import ExtractorError  # Импортируем исключение для модуля Extractor

class Extractor:
    """Унифицированный класс для работы с JSON задачами."""

    def __init__(self):
        pass  # Можно добавить инициализацию, если потребуется

    async def filter_tasks_by_value(self, tasks: List[Dict[str, Any]], filter_value: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Фильтрует задачи по значениям полей."""
        filtered_tasks = []

        for task in tasks:
            try:
                match_found = True
                for code, value in filter_value.items():
                    # Находим поле с нужным кодом
                    field = next((f for f in task.get("fields", []) if f.get("code") == code), None)
                    if not field:
                        match_found = False
                        break

                    # Проверяем значение
                    field_value = field.get("value")
                    field_type = field.get("type")
                    if field_type == "catalog":
                        if isinstance(value, str):
                            if field_value and 'values' in field_value and value in field_value['values']:
                                continue
                            else:
                                match_found = False
                                break
                        elif isinstance(value, dict):
                            for k, v in value.items():
                                if not isinstance(field_value, dict) or field_value.get(k) != v:
                                    match_found = False
                                    break
                            if not match_found:
                                break
                        else:
                            match_found = False
                            break
                    else:
                        if isinstance(value, dict):
                            for k, v in value.items():
                                if not isinstance(field_value, dict) or field_value.get(k) != v:
                                    match_found = False
                                    break
                        else:
                            if field_value != value:
                                match_found = False
                                break

                if match_found:
                    filtered_tasks.append(task)
            except Exception:
                # При ошибке в обработке конкретной задачи просто пропускаем её
                continue

        return filtered_tasks

    async def extract_task_fields(
        self,
        json_data: Union[str, Dict[str, Any], List[Dict[str, Any]]],
        return_field_codes: List[str]
    ) -> Dict[str, List[Any]]:
        """
        Извлекает и агрегирует значения полей задачи (или задач) по указанным кодам, включая вложенные структуры.
        
        Функция сама определяет, что ей передали:
        - JSON-строка (будет преобразована в объект),
        - Словарь с ключом "tasks" или "task",
        - Или даже сам объект задачи (если содержит ключ "fields"),
        - Либо список задач.

        :param json_data: JSON-строка или объект (словарь или список словарей) с задачами.
        :param return_field_codes: Список кодов полей, которые нужно извлечь.
        :return: Словарь, где ключи – коды полей, а значения – списки найденных значений.
        """
        
        # Если передана строка, пробуем преобразовать в объект
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError:
                raise ExtractorError("Ошибка: передана некорректная JSON-строка.")

        # Определяем, что передано: список или словарь
        if isinstance(json_data, list):
            tasks = json_data  # Уже список
        elif isinstance(json_data, dict):
            if "tasks" in json_data and isinstance(json_data["tasks"], list):
                tasks = json_data["tasks"]
            elif "task" in json_data and isinstance(json_data["task"], dict):
                tasks = [json_data["task"]]  # Превращаем в список
            elif "fields" in json_data:
                tasks = [json_data]  # Это объект задачи
            else:
                raise ExtractorError("Ошибка: JSON не содержит 'tasks' или 'task', либо не выглядит как задача (нет 'fields').")
        else:
            raise ExtractorError("Ошибка: JSON должен быть строкой, словарем или списком словарей.")

        # Инициализируем словарь для хранения извлеченных данных
        aggregated_fields = {code: [] for code in return_field_codes}

        def process_field(field: Dict[str, Any]):
            """Обрабатывает одно поле задачи, извлекая значение по его коду."""
            code = field.get("code")
            field_type = field.get("type")
            value = field.get("value")

            if code in return_field_codes:
                if field_type == "catalog" and isinstance(value, dict):
                    # Используем только первый уровень "rows", если он есть
                    rows = value.get("rows", [value])
                    aggregated_fields[code].extend(rows)
                elif field_type == "multiple_choice" and isinstance(value, dict):
                    aggregated_fields[code].extend(value.get("choice_names", value))
                elif field_type == "person" and isinstance(value, dict):
                    first_name = value.get("first_name", "")
                    last_name = value.get("last_name", "")
                    aggregated_fields[code].append(f"{first_name} {last_name}".strip())
                elif field_type == "file" and isinstance(value, list):
                    aggregated_fields[code].extend([
                        {"name": f.get("name"), "size": f.get("size")}
                        for f in value if "name" in f and "size" in f
                    ])
                elif field_type == "form_link" and isinstance(value, dict):
                    aggregated_fields[code].append(value.get("task_id", value))
                elif field_type == "table" and isinstance(value, list):
                    # Обрабатываем только верхний уровень строк таблицы
                    for row in value:
                        row_data = {
                            cell.get("code"): cell.get("value")
                            for cell in row.get("cells", [])
                            if cell.get("code") in return_field_codes
                        }
                        if row_data:
                            aggregated_fields[code].append(row_data)
                else:
                    aggregated_fields[code].append(value)

            # Рекурсивно обрабатываем вложенные поля в таблицах
            if field_type == "table" and isinstance(value, list):
                for row in value:
                    for cell in row.get("cells", []):
                        process_field(cell)

        # Обрабатываем каждую задачу
        for task in tasks:
            for field in task.get("fields", []):
                process_field(field)

        # Возвращаем только те ключи, для которых найдены значения
        return {code: values for code, values in aggregated_fields.items() if values}

    async def search_fields_by_codes_with_ids(
        self, task_details: Dict[str, Any], field_codes: List[str]
    ) -> Dict[str, str]:
        """Ищет поля по кодам и возвращает {id: type}"""
        target_codes = set(field_codes)
        result = {}

        def search_fields(fields):
            for field in fields:
                code = field.get("code")
                # Если код в списке искомых
                if code in target_codes:
                    try:
                        result[str(field["id"])] = field.get("type", "unknown")
                    except KeyError as e:
                        raise ExtractorError(f"Ошибка поиска поля: отсутствует 'id'. {str(e)}")
                
                # Рекурсивный поиск в таблицах
                if field.get("type") == "table":
                    for row in field.get("value", []):
                        search_fields(row.get("cells", []))

        # Проверяем, содержится ли задача в объекте или передана напрямую
        task_data = task_details.get("task", task_details)
        search_fields(task_data.get("fields", []))
        
        # Сохраняем порядок из field_codes и преобразуем ID в строки
        ordered_result = {}
        for code in field_codes:
            for field in task_data.get("fields", []):
                if field.get("code") == code:
                    try:
                        ordered_result[str(field["id"])] = field.get("type", "unknown")
                        break
                    except KeyError as e:
                        raise ExtractorError(f"Ошибка обработки поля: отсутствует 'id'. {str(e)}")
        
        return ordered_result