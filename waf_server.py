from flask import Flask, request, abort
import time

app = Flask(__name__)

# Словарь для хранения времени запросов по IP
visitors = {}
LIMIT = 5       # Максимум 5 запросов
WINDOW = 10     # В течение 10 секунд

@app.before_request
def limit_traffic():
    ip = request.remote_addr
    now = time.time()

    if ip not in visitors:
        visitors[ip] = []

    # Очищаем историю запросов, которые старше нашего окна (10 сек)
    visitors[ip] = [t for t in visitors[ip] if now - t < WINDOW]

    # Если лимит превышен — отбиваем запрос
    if len(visitors[ip]) >= LIMIT:
        abort(429) # Ошибка 429: Too Many Requests

    visitors[ip].append(now)

@app.route('/weather')
def weather():
    return "<h1>Погода: ясно, +20°C</h1>"

if __name__ == '__main__':
    # Запускаем локальный сервер
    app.run(port=5000)
