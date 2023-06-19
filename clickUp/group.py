import requests

# Функция для создания группы
def create_group(api_key, space_id, group_name):
    # Установите заголовок авторизации с помощью вашего токена API
    headers = {"Authorization": api_key}
    # Определите данные для создания группы
    data = {"name": group_name}
    # Отправьте POST-запрос для создания группы
    response = requests.post(f"https://api.clickup.com/api/v2/space/{space_id}/list", headers=headers, json=data)
    # Получите идентификатор созданной группы
    group_id = response.json()["id"]
    return group_id

# Функция для создания задачи
def create_task(api_key, list_id, task_name):
    # Установите заголовок авторизации с помощью вашего токена API
    headers = {"Authorization": api_key}
    # Определите данные для создания задачи
    data = {"name": task_name}
    # Отправьте POST-запрос для создания задачи
    response = requests.post(f"https://api.clickup.com/api/v2/list/{list_id}/task", headers=headers, json=data)
    # Получите идентификатор созданной задачи
    task_id = response.json()["id"]
    return task_id

# Функция для перемещения задачи в другую группу
def move_task(api_key, task_id, list_id):
    # Установите заголовок авторизации с помощью вашего токена API
    headers = {"Authorization": api_key}
    # Определите данные для перемещения задачи
    data = {"list_id": list_id}
    # Отправьте PUT-запрос для перемещения задачи
    response = requests.put(f"https://api.clickup.com/api/v2/task/{task_id}", headers=headers, json=data)

# Функция для сортировки задач по тегам
def sort_tasks_by_tag(api_key, space_id):
    # Установите заголовок авторизации с помощью вашего токена API
    headers = {"Authorization": api_key}
    # Отправьте GET-запрос для получения всех задач в пространстве
    response = requests.get(f"https://api.clickup.com/api/v2/space/{space_id}/task", headers=headers)
    # Преобразуйте ответ в формат JSON
    tasks = response.json()["tasks"]
    # Создайте словарь для хранения задач, сгруппированных по тегам
    tasks_by_tag = {}
    # Пройдитесь по каждой задаче и добавьте ее в соответствующую группу по тегу
    for task in tasks:
        for tag in task["tags"]:
            tag_name = tag["name"]
            if tag_name not in tasks_by_tag:
                # Если группа не существует, создайте ее
                list_id = create_group(api_key, space_id, tag_name)
                tasks_by_tag[tag_name] = {"list_id": list_id, "tasks": []}
            tasks_by_tag[tag_name]["tasks"].append(task)
    # Создайте задачи для каждой группы
    for tag_name in tasks_by_tag:
        list_id = tasks_by_tag[tag_name]["list_id"]
        for task in tasks_by_tag[tag_name]["tasks"]:
            task_name = task["name"]
            task_id = create_task(api_key, list_id, task_name)
            move_task(api_key, task_id, list_id)
    # Верните словарь с задачами, сгруппированными по тегам
    return tasks_by_tag