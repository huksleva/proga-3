# myapp.py

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

# Получаем путь к папке templates (относительно текущего файла)
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

# Импортируем модели
from models import App, Author, User, Currency, UserCurrency

# Импортируем функцию получения валют
from utils.currencies_api import get_currencies

# --- ГЛОБАЛЬНЫЕ ОБЪЕКТЫ ---

# Инициализируем Environment с FileSystemLoader
env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape()
)


# Загружаем шаблоны
template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_currencies = env.get_template("currencies.html")
template_user_detail = env.get_template("user_detail.html")
template_author = env.get_template("author.html")

# Создаём экземпляры приложения и автора
main_author = Author(name="Леонид", group="ИВТ 2", age=20, sex="М")
main_app = App(name="PROGA3", version="2.0", author=main_author)

# --- ВРЕМЕННЫЕ ДАННЫЕ (для примера) ---
# В реальном приложении данные должны браться из БД или файла
users = [
    User(username="Анна", i_d=1),
    User(username="Борис", i_d=2),
    User(username="Виктория", i_d=3)
]

# Подписки пользователей (UserCurrency)
subscriptions = [
    UserCurrency(id=1, user_id=1, currency_id="R01235"),  # USD
    UserCurrency(id=2, user_id=1, currency_id="R01239"),  # EUR
    UserCurrency(id=3, user_id=2, currency_id="R01235"),  # USD
]

# --- КЛАСС ОБРАБОТЧИКА ЗАПРОСОВ ---

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET-запросов"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == "/":
            self.handle_index()
        elif path == "/users":
            self.handle_users()
        elif path == "/author":
            self.handle_author()
        elif path == "/currencies":
            self.handle_currencies()
        elif path == "/user" and "id" in query_params:
            user_id = int(query_params["id"][0])
            self.handle_user(user_id)
        else:
            self.send_error(404, "Страница не найдена")

    def handle_index(self):
        """Главная страница"""
        html_content = template_index.render(
            app_name=main_app.name,
            app_version=main_app.version,
            author_name=main_app.author.name,
            group=main_app.author.group,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html_content)

    def handle_users(self):
        """Список пользователей"""
        html_content = template_users.render(
            users=users,
            app_name=main_app.name,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html_content)

    def handle_user(self, user_id: int):
        """Информация о конкретном пользователе и его подписках"""
        user = next((u for u in users if u.i_d == user_id), None)
        if not user:
            self.send_error(404, f"Пользователь с ID={user_id} не найден")
            return

        # Находим подписки пользователя
        user_subscriptions = [sub for sub in subscriptions if sub.user_id == user_id]
        # Находим объекты валют по их ID
        all_currencies = get_currencies()  # получаем актуальные курсы
        subscribed_currencies = [
            next((cur for cur in all_currencies if cur.identification_number == sub.currency_id), None)
            for sub in user_subscriptions
        ]

        html_content = template_user_detail.render(
            user=user,
            currencies=subscribed_currencies,
            app_name=main_app.name,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html_content)

    def handle_currencies(self):
        """Список валют с текущими курсами"""
        currencies = get_currencies()  # получаем свежие курсы

        html_content = template_currencies.render(
            currencies=currencies,
            app_name=main_app.name,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html_content)

    def handle_author(self):
        """Информация об авторе"""
        html_content = template_author.render(
            author=main_app.author,
            app_name=main_app.name,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html_content)

    def send_html_response(self, html_content: str):
        """Отправка HTML-ответа"""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_error(self, code: int, message: str = ""):
        """Отправка ошибки"""
        self.send_response(code)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        error_page = f"<h1>{code}</h1><p>{message}</p>"
        self.wfile.write(error_page.encode("utf-8"))


# --- ЗАПУСК СЕРВЕРА ---

if __name__ == "__main__":
    server_address = ("", 8000)  # localhost:8000
    httpd = HTTPServer(server_address, MyRequestHandler)
    print("Сервер запущен на http://localhost:8000")
    httpd.serve_forever()