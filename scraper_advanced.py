import requests
import time
from bs4 import BeautifulSoup

# Заголовки (Headers) нужны, чтобы сайт думал, что к нему обращается обычный человек через браузер
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

url = 'https://example.com' # Вписываем url искомого сайта

try:
    response = requests.get(url, headers=headers, timeout=15) # Увеличим таймаут на всякий случай
    print(f"Статус код для {url}: {response.status_code}")
    if response.status_code == 200:
        print("Успешно получено содержимое страницы.")
    else:
        print("Не удалось получить содержимое страницы. Возможно, сайт блокирует запросы или произошла другая ошибка.")
except requests.exceptions.ConnectionError as e:
    print(f"Ошибка соединения: {e}. Возможно, сайт активно блокирует запросы или есть проблемы с сетью.")
except requests.exceptions.Timeout as e:
    print(f"Превышен таймаут: {e}. Сервер не ответил за отведенное время.")
except requests.exceptions.RequestException as e:
    print(f"Произошла общая ошибка запроса: {e}")
# вписываем стартовый и конечный айди страницы для поиска информации по сайту
start_id = 1
end_id = 10

print(f"Начинаем искать от {start_id} до {end_id}...\n")

for object_id in range(start_id, end_id + 1):
    result = get_object_title(str(object_id))

    # 2. Выводим найденный url
    current_url = f"https://example.com/{object_id}/"


    # 3. Даем перерыв между запросами
    time.sleep(1)
