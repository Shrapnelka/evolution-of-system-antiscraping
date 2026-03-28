import requests

from bs4 import BeautifulSoup

# Заголовки (Headers) нужны, чтобы сайт думал, что к нему обращается обычный человек через браузер
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# Функция для извлечения температуры: проверяет атрибут 'value' или берет текст
def get_temp(element):
    if not element:
        return '?'
    val = element.get('value')
    return val if val is not None else element.get_text(strip=True)

try:
    # Делаем НОВЫЙ запрос при каждом запуске ячейки, чтобы данные были актуальными
    response = requests.get('https://www.gismeteo.ru/weather-moscow-4368/', headers=headers, timeout=10)
    second_reponse = requests.get('https://www.gismeteo.ru/weather-moscow-4368/4-day/', headers=headers, timeout=10)
    # Создаем объект soup для поиска по HTML коду
    soup = BeautifulSoup(response.text, 'html.parser')
    new_soup = BeautifulSoup(second_reponse.text, 'html.parser')

    # Ищем заголовок с названием города
    city = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Город не найден'
    print(city)

    print('\n--- ПОГОДА ---')
    # Ищем все карточки (плитки) с прогнозом на дни
    day_cards = soup.select('.weathertabs .weathertab') + new_soup.select('.weathertabs .weathertab')

    forecast_lines = []

    # Проходим циклом по первым 5 карточкам
    for i, card in enumerate(day_cards[:6]):
        # Вытаскиваем название дня (Завтра, Пн) и дату
        day_name = card.select_one('.day').get_text(strip=True) if card.select_one('.day') else ''
        day_date = card.select_one('.date').get_text(strip=True) if card.select_one('.date') else ''

        # Состояние берем из data-tooltip карточки
        day_status = card.get('data-tooltip', 'состояние не указано')

        # Ищем все теги температуры
        temps = card.find_all('temperature-value')

        if i == 0:
            # Для текущего момента выводим только одну (текущую) температуру
            t_now = get_temp(temps[0]) if len(temps) > 0 else '?'
            line = f"{'Сейчас'.ljust(15)} | Текущая: {t_now.rjust(3)}°C | {day_status}"
        else:
            # Для остальных дней выводим Днём/Ночью
            full_date = f"{day_name} {day_date}".strip() or "?"
            t_day = get_temp(temps[1]) if len(temps) > 0 else '?'
            t_night = get_temp(temps[0]) if len(temps) > 1 else '?'
            line = f"{full_date.ljust(15)} | Днём:{t_day.rjust(3)}°C | Ночью:{t_night.rjust(3)}°C | {day_status}"

        print(line)
        forecast_lines.append(line)

except Exception as e:
    print(f"Ошибка обновления: {e}")
