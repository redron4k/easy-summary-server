import requests
import time
import random
import json
from datetime import datetime
# Основные настройки
BASE_URL = "http://localhost:8000/save_summary"
TARGET_SIZE_MB = 100
TEXT_SIZE_KB = 100
REQUEST_TIMEOUT = 10
MAX_REQUESTS = 100

def generate_valid_utf8_text(size_kb):
    """Генерация случайного текста заданного размера."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
block = ''.join(random.choice(chars) for _ in range(int(size_kb * 1024)))
    return block

def send_request(text_size_kb):
    """Отправка POST-запроса с текстом указанного размера."""
    text = generate_valid_utf8_text(text_size_kb)
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(BASE_URL, data=json.dumps(payload).encode('utf-8'), headers=headers, timeout=REQUEST_TIMEOUT)
        return response.ok
    except requests.RequestException:
        return False

def run_throughput_test():
    """Основной цикл отправки запросов и измерения производительности."""
    total_data_sent = 0
    successful_requests = 0
    start_time = time.time()
    for request_number in range(MAX_REQUESTS):
        success = send_request(TEXT_SIZE_KB)
        total_data_sent += TEXT_SIZE_KB * 1024  # Добавляем объем отправленного текста
        if success:
            successful_requests += 1
        # Проверяем, достигли ли мы целевого объема
        if total_data_sent >= TARGET_SIZE_MB * 1024 * 1024:
            break

end_time = time.time()
    duration = end_time - start_time    
throughput_mbps = (total_data_sent / (1024 * 1024)) / duration
    success_rate = successful_requests / MAX_REQUESTS * 100
    print(f"\nТест завершён.")
    print(f"Время выполнения: {duration:.2f} секунд")
    print(f"Успешных запросов: {successful_requests}/{MAX_REQUESTS} ({success_rate:.1f}%)")
if __name__ == "__main__":
    run_throughput_test()
