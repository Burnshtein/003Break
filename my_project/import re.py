import re
import os

def create_user():
    """
    Функция для создания нового пользователя.
    """
    print("\nСоздание нового пользователя")
    print("=" * 40)
    
    college = input("Введите название колледжа: ").strip()
    course = input("Введите название курса: ").strip()
    name = input("Введите ФИО: ").strip()
    group = input("Введите группу/команду: ").strip()
    user_id = input("Введите ID: ").strip()
    
    # Создаем содержимое файла
    content = f"""Колледж: {college}
Курс: {course}
ФИ: {name}
Команда: {group}
ID: {user_id}"""
    
    # Сохраняем в файл
    file_path = 'README003.md'
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Пользователь создан! Данные сохранены в файл: {file_path}")
        return college, course, name, group, user_id
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return None, None, None, None, None

def find_user_in_file(file_path, target_name):
    """
    Функция для поиска пользователя в файле по ФИО.
    Возвращает данные пользователя если найден, иначе None.
    """
    try:
        # Пробуем разные кодировки
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    break
            except UnicodeDecodeError:
                continue
        else:
            return None
            
        # Ищем пользователя по ФИО
        name_patterns = [r'ФИ[:\s]*([^\n]+)', r'ФИО[:\s]*([^\n]+)', r'Name[:\s]*([^\n]+)', r'Имя[:\s]*([^\n]+)']
        
        for pattern in name_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if target_name.lower() in match.lower():
                    # Нашли пользователя, извлекаем все его данные
                    return extract_user_data(content)
        
        return None
                
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def extract_user_data(content):
    """
    Извлекает все данные пользователя из содержимого файла.
    """
    patterns = {
        'college': [r'Колледж[:\s]*([^\n]+)', r'College[:\s]*([^\n]+)', r'Учебное заведение[:\s]*([^\n]+)'],
        'course': [r'Курс[:\s]*([^\n]+)', r'Course[:\s]*([^\n]+)'],
        'name': [r'ФИ[:\s]*([^\n]+)', r'ФИО[:\s]*([^\n]+)', r'Name[:\s]*([^\n]+)', r'Имя[:\s]*([^\n]+)'],
        'group': [r'Команда[:\s]*([^\n]+)', r'Группа[:\s]*([^\n]+)', r'Group[:\s]*([^\n]+)', r'Team[:\s]*([^\n]+)'],
        'id': [r'ID[:\s]*([^\n]+)', r'ИД[:\s]*([^\n]+)', r'Номер[:\s]*([^\n]+)', r'№[:\s]*([^\n]+)']
    }
    
    found_data = {}
    for field_name, field_patterns in patterns.items():
        for pattern in field_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                found_data[field_name] = match.group(1).strip()
                break
    
    # Проверяем, что все данные найдены
    if all(key in found_data for key in ['college', 'course', 'name', 'group', 'id']):
        return (
            found_data['college'],
            found_data['course'],
            found_data['name'],
            found_data['group'],
            found_data['id']
        )
    
    return None

def main():
    """
    Главная функция программы.
    """
    print("Программа для работы с пользовательскими данными")
    print("=" * 50)
    
    file_path = 'README003.md'
    
    while True:
        print("\nВыберите действие:")
        print("1. Поиск пользователя по ФИО")
        print("2. Создать нового пользователя")
        print("3. Показать всех пользователей в файле")
        print("4. Выйти")
        
        choice = input("Ваш выбор (1-4): ").strip()
        
        if choice == '4':
            print("До свидания!")
            break
            
        elif choice == '1':
            target_name = input("Введите ФИО для поиска: ").strip()
            
            if not target_name:
                print("ФИО не может быть пустым!")
                continue
            
            # Ищем пользователя в файле
            user_data = find_user_in_file(file_path, target_name)
            
            if user_data:
                college, course, name, group, user_id = user_data
                print(f"\nПользователь найден!")
                print_user_greeting(college, course, name, group, user_id)
            else:
                print(f"\nПользователь '{target_name}' не найден в файле.")
                create_new = input("Хотите создать нового пользователя? (да/нет): ").strip().lower()
                if create_new in ['да', 'yes', 'y', 'д']:
                    college, course, name, group, user_id = create_user()
                    if all([college, course, name, group, user_id]):
                        print_user_greeting(college, course, name, group, user_id)
        
        elif choice == '2':
            college, course, name, group, user_id = create_user()
            if all([college, course, name, group, user_id]):
                print_user_greeting(college, course, name, group, user_id)
        
        elif choice == '3':
            print("\nВсе пользователи в файле:")
            print("=" * 50)
            show_all_users(file_path)
        
        else:
            print("Неверный выбор. Попробуйте снова.")
            continue
        
        # Предложение продолжить работу
        another = input("\nХотите продолжить работу? (да/нет): ").strip().lower()
        if another not in ['да', 'yes', 'y', 'д']:
            print("До свидания!")
            break

def show_all_users(file_path):
    """
    Показывает всех пользователей из файла.
    """
    try:
        # Пробуем разные кодировки
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    break
            except UnicodeDecodeError:
                continue
        else:
            print("Не удалось прочитать файл")
            return
        
        # Ищем все записи с ФИО
        name_patterns = [r'ФИ[:\s]*([^\n]+)', r'ФИО[:\s]*([^\n]+)', r'Name[:\s]*([^\n]+)', r'Имя[:\s]*([^\n]+)']
        all_names = []
        
        for pattern in name_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            all_names.extend(matches)
        
        if all_names:
            for i, name in enumerate(set(all_names), 1):
                print(f"{i}. {name.strip()}")
        else:
            print("В файле нет записей о пользователях")
            
    except FileNotFoundError:
        print("Файл не существует")
    except Exception as e:
        print(f"Ошибка: {e}")

def print_user_greeting(college, course, name, group, user_id):
    """
    Функция для вывода приветствия пользователя.
    """
    print("\nВсе данные успешно получены!")
    print("=" * 50)
    print(f"ФИО: {name}")
    print(f"Колледж: {college}")
    print(f"Курс: {course}")
    print(f"Группа/Команда: {group}")
    print(f"ID: {user_id}")
    print("=" * 50)
    print("Добро пожаловать!")

# Запуск программы
if __name__ == "__main__":
    main()