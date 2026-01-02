# myapp.py

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

# Импорт моделей
from models import App, Author, User, UserCurrency
from utils.currencies_api import get_currencies

# === Настройка Jinja2 ===
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape()
)

# Загрузка шаблонов (все обязательные по заданию)
template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user_detail = env.get_template("user_detail.html")
template_currencies = env.get_template("currencies.html")
template_author = env.get_template("author.html")

# === Глобальные объекты ===
main_author = Author(name="Леонид", group="ИВТ 2", age=20, sex="М")
main_app = App(name="PROGA3", version="2.0", author=main_author)

# === Тестовые данные ===
users = [
    User(username="Анна", i_d=1),
    User(username="Борис", i_d=2),
    User(username="Виктория", i_d=3)
]

subscriptions = [
    UserCurrency(id=1, user_id=1, currency_id="R01235"),  # USD
    UserCurrency(id=2, user_id=1, currency_id="R01239"),  # EUR
    UserCurrency(id=3, user_id=2, currency_id="R01235"),  # USD
]

# === Обработчик запросов ===
class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
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
            try:
                user_id = int(query_params["id"][0])
                self.handle_user(user_id)
            except (ValueError, IndexError):
                self.send_error(400, "Неверный ID пользователя")
        else:
            self.send_error(404, "Страница не найдена")

    def handle_index(self):
        html = template_index.render(
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
        self.send_html_response(html)

    def handle_users(self):
        html = template_users.render(
            users=users,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html)

    def handle_user(self, user_id: int):
        user = next((u for u in users if u.i_d == user_id), None)
        if not user:
            self.send_error(404, f"Пользователь с ID={user_id} не найден")
            return

        user_subscriptions = [sub for sub in subscriptions if sub.user_id == user_id]
        all_currencies = get_currencies()
        subscribed_currencies = [
            next((cur for cur in all_currencies if cur.identification_number == sub.currency_id), None)
            for sub in user_subscriptions
        ]

        html = template_user_detail.render(
            user=user,
            currencies=subscribed_currencies,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html)

    def handle_currencies(self):


        currencies = get_currencies()

        html = template_currencies.render(
            currencies=currencies,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html)

    def handle_author(self):
        html = template_author.render(
            author=main_app.author,
            navigation=[
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Автор", "href": "/author"},
                {"caption": "Валюты", "href": "/currencies"}
            ]
        )
        self.send_html_response(html)

    def send_html_response(self, content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_error(self, code, message=None, explain=None):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # Формируем сообщение (можно использовать message или explain)
        if message is None:
            if code == 404:
                message = "Страница не найдена"
            elif code == 400:
                message = "Неверный запрос"
            else:
                message = "Ошибка сервера"

        error_html = f"<h1>{code} Error</h1><p>{message}</p><a href='/'>← На главную</a>"
        self.wfile.write(error_html.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("", 8000), MyRequestHandler) # type: ignore
    print("Сервер запущен на http://localhost:8000")
    print("Поддерживаемые маршруты:")
    print("  /")
    print("  /users")
    print("  /user?id=1")
    print("  /currencies")
    print("  /author")
    server.serve_forever()