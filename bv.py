import requests
import json
import base64
import webbrowser
import urllib.parse

def get_user_repo_info(username):
    """
    Получает информацию о репозитории пользователя и README файл
    """
    # URL для получения информации о пользователе
    user_url = f"https://api.github.com/users/{username}"
    
    try:
        # Получаем информацию о пользователе
        user_response = requests.get(user_url)
        
        # Если пользователь не найден (статус 404)
        if user_response.status_code == 404:
            return None, "Пользователь не найден", None
            
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Получаем список репозиториев пользователя
        repos_url = user_data['repos_url']
        repos_response = requests.get(repos_url)
        repos_response.raise_for_status()
        repos_data = repos_response.json()
        
        # Ищем репозиторий с именем пользователя (обычно это основной репозиторий)
        personal_repo = None
        for repo in repos_data:
            if repo['name'].lower() == username.lower():
                personal_repo = repo
                break
        
        # Если не нашли репозиторий с именем пользователя, берем первый репозиторий
        if not personal_repo and repos_data:
            personal_repo = repos_data[0]
        
        if not personal_repo:
            return None, "У пользователя нет репозиториев", None
        
        # Получаем README файл
        readme_url = f"https://api.github.com/repos/{username}/{personal_repo['name']}/readme"
        readme_response = requests.get(readme_url)
        
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            # Декодируем содержимое README из base64
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        else:
            readme_content = "README файл не найден"
        
        return user_data, readme_content, personal_repo['name']
        
    except requests.exceptions.RequestException as e:
        return None, f"Ошибка при подключении к GitHub: {e}", None
    except json.JSONDecodeError:
        return None, "Ошибка при обработке данных", None

def collect_registration_data():
    """
    Собирает данные для регистрации у пользователя
    """
    print("\n📝 Давайте подготовим данные для регистрации на GitHub!")
    print("=" * 50)
    
    registration_data = {}
    
    # Собираем основные данные
    registration_data['username'] = input("Придумайте имя пользователя: ").strip()
    registration_data['email'] = input("Введите ваш email: ").strip()
    registration_data['password'] = input("Придумайте пароль (минимум 8 символов): ").strip()
    
    # Дополнительная информация
    print("\n💡 Дополнительная информация (можно пропустить, нажав Enter):")
    registration_data['name'] = input("Ваше полное имя: ").strip()
    registration_data['newsletter'] = input("Подписаться на рассылку GitHub? (y/n): ").strip().lower() == 'y'
    
    return registration_data

def validate_registration_data(data):
    """
    Проверяет корректность данных для регистрации
    """
    errors = []
    
    if len(data['username']) < 1:
        errors.append("Имя пользователя не может быть пустым")
    elif len(data['username']) > 39:
        errors.append("Имя пользователя слишком длинное (макс. 39 символов)")
    
    if '@' not in data['email'] or '.' not in data['email']:
        errors.append("Некорректный email адрес")
    
    if len(data['password']) < 8:
        errors.append("Пароль должен содержать минимум 8 символов")
    
    return errors

def open_registration_page(data):
    """
    Открывает страницу регистрации с предзаполненными данными
    """
    # Создаем URL с параметрами
    params = {
        'user_login': data['username'],
        'user_email': data['email']
    }
    
    # Кодируем параметры для URL
    query_string = urllib.parse.urlencode(params)
    registration_url = f"https://github.com/signup?{query_string}"
    
    print(f"\n🎯 Открываю страницу регистрации с вашими данными...")
    print(f"🔗 {registration_url}")
    
    # Открываем в браузере
    webbrowser.open(registration_url)
    
    print("\n📋 Ваши данные для копирования:")
    print(f"👤 Имя пользователя: {data['username']}")
    print(f"📧 Email: {data['email']}")
    print(f"🔑 Пароль: {data['password']}")
    
    if data['name']:
        print(f"👨‍💼 Полное имя: {data['name']}")

def offer_registration(username):
    """
    Предлагает и помогает с регистрацией на GitHub
    """
    print(f"\n🤔 Пользователь '{username}' не найден на GitHub!")
    print("=" * 50)
    
    choice = input("Хотите зарегистрироваться на GitHub? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes', 'да', 'д']:
        # Собираем данные для регистрации
        registration_data = collect_registration_data()
        
        # Проверяем данные
        errors = validate_registration_data(registration_data)
        if errors:
            print("\n❌ Ошибки в данных:")
            for error in errors:
                print(f"   - {error}")
            print("Пожалуйста, попробуйте снова.")
            return
        
        # Открываем страницу регистрации
        open_registration_page(registration_data)
        
        print("\n✅ После регистрации вернитесь в программу!")
        print("💡 Совет: сохраните ваши данные в надежном месте")
        
    else:
        print("\n👌 Хорошо! Проверьте правильность введенного имени.")

def process_user(username):
    """
    Обрабатывает запрос для одного пользователя
    """
    print(f"\n🔍 Ищем пользователя {username} на GitHub...")
    
    # Получаем информацию о пользователе и его README
    user_data, readme_content, repo_name = get_user_repo_info(username)
    
    if user_data is None:
        if readme_content == "Пользователь не найден":
            print(f"👋 Здравствуйте!")
            offer_registration(username)
        else:
            print(f"❌ {readme_content}")
        return
    
    # Выводим приветствие с информацией о пользователе
    print("\n" + "=" * 50)
    print(f"🎉 Приветствуем, {user_data.get('name', username)}!")
    print(f"📝 Биография: {user_data.get('bio', 'Не указана')}")
    print(f"📍 Местоположение: {user_data.get('location', 'Не указано')}")
    print(f"🔗 Профиль: {user_data['html_url']}")
    if repo_name:
        print(f"📂 Репозиторий: {repo_name}")
    print("=" * 50)
    
    # Выводим содержимое README
    if readme_content and readme_content != "README файл не найден":
        print("\n📖 Содержимое README файла:")
        print("-" * 30)
        # Ограничиваем вывод до первых 500 символов
        preview = readme_content[:500] + "..." if len(readme_content) > 500 else readme_content
        print(preview)
        if len(readme_content) > 500:
            print("... (показаны первые 500 символов)")
    
    print("\n" + "=" * 50)
    print("✨ Приятного кодирования!")

def main():
    """
    Основная функция программы
    """
    print("👋 Добро пожаловать в GitHub приветственную программу!")
    print("=" * 50)
    print("Введите 'exit' или 'quit' для выхода из программы")
    print("=" * 50)
    
    while True:
        # Получаем имя пользователя
        username = input("\nВведите имя пользователя GitHub: ").strip()
        
        # Проверяем команды выхода
        if username.lower() in ['exit', 'quit', 'выход']:
            print("👋 До свидания!")
            break
            
        if not username:
            print("❌ Имя пользователя не может быть пустым!")
            continue
        
        # Обрабатываем пользователя
        process_user(username)

if __name__ == "__main__":
    main()