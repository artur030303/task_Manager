MAIN_PRIORITY = {"1": "низкий", "2": "средний", "3": "высокий"}
MAIN_STATUS = {"1": "новая", "2": "в процессе", "3": "завершена"}

task_manager = {}


def save_tasks() -> str:
    with open("file_tasks.txt", 'w') as file:
        for task_id, task in task_manager.items():
            delimeter = '=' * 200
            title = task['title'][:30].ljust(30)
            description = task['description'][:100].ljust(100)
            priority = task['priority'][:7].ljust(7)
            line = f"{task_id.ljust(5)}|{title}|{description}|{
                priority}|{task['status']}\n{delimeter}"
            file.write(line + '\n')


def load_tasks() -> dict:
    try:
        with open("file_tasks.txt", 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    task_id, title, description, priority, status = parts
                    task_manager[task_id] = {
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "status": status,
                    }
    except FileNotFoundError:
        print("Начинаем с пустого списка.")


def next_new_id() -> int:
    if task_manager:
        return max(int(id) for id in task_manager) + 1
    return 1


def create_task() -> None:
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    while True:
        priority = input(
            "Выберите приоритет (1 - низкий, 2 - средний, 3 - высокий): ")
        if priority == '1' or priority == '2' or priority == '3':
            break
        else:
            print("Приоритет может быть только 1,2 или 3!Введите заново")
    while True:
        status = input(
            "Выберите статус (1 - новая, 2 - в процессе, 3 - завершена): ")
        if status == '1' or status == '2' or status == '3':
            break
        else:
            print("Статус может быть только 1,2 или 3!Введите заново")

    task_id = str(next_new_id())
    task_manager[task_id] = {
        "title": title,
        "description": description,
        "priority": MAIN_PRIORITY[priority],
        "status": MAIN_STATUS[status],
    }
    save_tasks()
    print("Задача добавлена.")


def update_task(task_id: str) -> dict:
    if task_id not in task_manager:
        print("Задача с таким ID не найдена.")
        return

    new_title = input("Введите новое название задачи: ")
    new_description = input("Введите новое описание задачи: ")
    new_priority = input(
        "Выберите новый приоритет (1 - низкий, 2 - средний, 3 - высокий): ")
    new_status = input(
        "Выберите новый статус (1 - новая, 2 - в процессе, 3 - завершена): ")

    if new_priority not in MAIN_PRIORITY or new_status not in MAIN_STATUS:
        print("Ошибка: Некорректный приоритет или статус.")
        return

    task_manager[task_id] = {
        "title": new_title,
        "description": new_description,
        "priority": MAIN_PRIORITY[new_priority],
        "status": MAIN_STATUS[new_status],
    }
    save_tasks()
    print("Задача обновлена.")


def delete_task(task_id: str) -> None:
    if task_id in task_manager:
        del task_manager[task_id]
        save_tasks()
        print(f"Задача с ID {task_id} удалена.")
    else:
        print("Задача с таким ID не найдена.")


def view_tasks() -> dict:
    if not task_manager:
        print("Список задач пуст.")
        return

    while True:
        print("Просмотр задач:")
        print("1. Отобразить задачи в изначальном виде")
        print("2. Отсортировать по статусу")
        print("3. Отсортировать по приоритету")
        print("4. Осуществить поиск по названию или описанию")
        print("0. Вернуться в главное меню")

        выбор = input("Выберите действие: ")

        if выбор == "1":
            print_tasks(task_manager)
        elif выбор == "2":
            sorted_tasks = sorted(task_manager.items(),
                                  key=lambda x: x[1]["status"])
            print_tasks(dict(sorted_tasks))
        elif выбор == "3":
            sorted_tasks = sorted(
                task_manager.items(), key=lambda x: x[1]["priority"])
            print_tasks(dict(sorted_tasks))
        elif выбор == "4":
            search_term = input("Введите значение для поиска: ").lower()
            filtered_tasks = {task_id: task for task_id, task in task_manager.items()
                              if search_term in task["title"].lower() or search_term in task["description"].lower()}
            print_tasks(filtered_tasks)
        elif выбор == "0":
            break
        else:
            print("Такой функции нет.Попробуйте снова.")


def print_tasks(tasks: dict) -> str:
    if not tasks:
        print("Список задач пуст.")
        return

    for task_id, task in tasks.items():
        print(f"ID: {task_id}")
        print(f"Название: {task['title']}")
        print(f"Описание: {task['description']}")
        print(f"Приоритет: {task['priority']}")
        print(f"Статус: {task['status']}")


load_tasks()


while True:
    print("Меню:")
    print("1. Создать задачу")
    print("2. Обновить задачу")
    print("3. Удалить задачу")
    print("4. Просмотреть задачи")
    print("0. Выйти")

    choice = input("Выберите действие: ")

    if choice == "1":
        create_task()
    elif choice == "2":
        task_id = input("Введите ID задачи для обновления: ")
        update_task(task_id)
    elif choice == "3":
        task_id = input("Введите ID задачи для удаления: ")
        delete_task(task_id)
    elif choice == "4":
        view_tasks()
    elif choice == "0":
        break
    else:
        print("Такой функции нет.Попробуйте снова.")
