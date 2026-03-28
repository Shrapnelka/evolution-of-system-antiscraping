import requests
import time

url = 'http://127.0.0.1:5000/weather'

print("Начинаем парсинг...\n")

for i in range(1, 10):
    try:
        response = requests.get(url, timeout=2)

        if response.status_code == 200:
            print(f"Запрос {i}: Успешно. Данные получены.")
        elif response.status_code == 429:
            print(f"Запрос {i}: БЛОКИРОВКА WAF! Ошибка 429 Too Many Requests.")
            print("Скрипт остановлен системой защиты.")
            break

        time.sleep(0.2) # Маленькая задержка, чтобы эмулировать работу скрипта

    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        break
