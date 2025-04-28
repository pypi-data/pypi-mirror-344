from deepdiff import DeepDiff


def format_diff(diff: dict) -> str:
    """
    Форматирует результат DeepDiff в формат, похожий на git diff.
    """
    result = []

    if "values_changed" in diff:
        for path, change in diff["values_changed"].items():
            old_value = change["old_value"]
            new_value = change["new_value"]
            result.append(f"--- {path}: {old_value} ---")
            result.append(f"+++ {path}: {new_value} +++")

    if "dictionary_item_added" in diff:
        for path in diff["dictionary_item_added"]:
            result.append(f"+++ {path}: добавлено +++")

    if "dictionary_item_removed" in diff:
        for path in diff["dictionary_item_removed"]:
            result.append(f"--- {path}: удалено ---")

    if "iterable_item_added" in diff:
        for path, value in diff["iterable_item_added"].items():
            result.append(f"+++ {path}: {value} +++")

    if "iterable_item_removed" in diff:
        for path, value in diff["iterable_item_removed"].items():
            result.append(f"--- {path}: {value} ---")

    if "type_changes" in diff:
        for path, change in diff["type_changes"].items():
            old_type = change["old_type"]
            new_type = change["new_type"]
            result.append(f"--- {path}: тип изменен с {old_type} на {new_type} ---")

    return "\n".join(result)


def get_diff(expected: any, actual: any) -> str:
    """
    Возвращает строку с различиями между ожидаемым и текущим значением в формате, похожем на git diff.
    """
    diff = DeepDiff(expected, actual, ignore_order=True)

    if not diff:
        return "Значения совпадают"

    return format_diff(diff)
