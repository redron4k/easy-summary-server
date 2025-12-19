import requests
import time
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
class LoadTester:
    def __init__(self, base_url, start_rate=1, max_rate=50, step=1, timeout=5):
        self.base_url = base_url
        self.current_rate = start_rate
        self.max_rate = max_rate
        self.step = step
        self.timeout = timeout
        self.is_running = True
   
    def _make_request(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        try:
            start_time = time.time()
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            elapsed_time = time.time() - start_time
            success = response.status_code in (200, 201)
            return {
                "success": success,
                "status_code": response.status_code,
                "response_time": elapsed_time,
                "endpoint": endpoint,
                "data": response.json() if response.content else None,
                "error": None if success else f"HTTP {response.status_code}"
            }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout", "response_time": self.timeout, "endpoint": endpoint}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "ConnectionError", "response_time": 0, "endpoint": endpoint}
        except Exception as e:
            return {"success": False, "error": str(e), "response_time": 0, "endpoint": endpoint}
  
    def make_summarize_request(self):
        paragraphs = [
            "Машинное обучение — это область искусственного интеллекта, которая позволяет компьютерам обучаться на основе данных без явного программирования. ",
            "Нейронные сети имитируют работу человеческого мозга и используются для решения сложных задач, таких как распознавание изображений и обработка естественного языка. ",
            "API (Application Programming Interface) — это набор протоколов и инструментов для создания программного обеспечения, который позволяет различным приложениям взаимодействовать друг с другом. "
        ]
        text = "".join(random.sample(paragraphs, random.randint(1, 3)))
        return self._make_request("summarize", {"text": text})
   
    def make_save_summaries_request(self):
        sample_texts = [
            "Климатические изменения — одна из самых серьезных проблем современности. Повышение температуры, экстремальные погодные явления и повышение уровня моря оказывают значительное влияние на экосистемы и человеческое общество.",
            "Искусственный интеллект трансформирует различные отрасли, от здравоохранения до финансов. Машинное обучение позволяет анализировать большие данные и принимать более обоснованные решения.",
            ]
        return self._make_request("save_summary", {"text": random.choice(sample_texts), "token": random.randint(1000, 9999)})
  
    def run_phase(self, rate):
        results = []
        with ThreadPoolExecutor(max_workers=min(rate, 50)) as executor:
            futures = [executor.submit(random.choice([self.make_summarize_request, self.make_save_summaries_request])) for _ in range(rate)]
            for future in as_completed(futures):
                results.append(future.result())     
        successful = sum(1 for r in results if r.get("success"))
        failed = len(results) - successful 
        summarize_stats = [r for r in results if r.get("endpoint") == "summarize"]
        save_stats = [r for r in results if r.get("endpoint") == "save_summary"]  
        successful_summarize = sum(1 for r in summarize_stats if r.get("success"))
        successful_save = sum(1 for r in save_stats if r.get("success"))
        print(f"[{time.strftime('%H:%M:%S')}] Успешно: {successful}/{rate} (summarize: {successful_summarize}/{len(summarize_stats)}, save_summaries: {successful_save}/{len(save_stats)})")
        if successful > 0:
            successful_responses = [r for r in results if r.get("success")]
            avg_time = sum(r.get("response_time", 0) for r in successful_responses) / successful
            summarize_times = [r.get("response_time", 0) for r in summarize_stats if r.get("success")]
            save_times = [r.get("response_time", 0) for r in save_stats if r.get("success")]
            avg_summarize = sum(summarize_times) / len(summarize_times) if summarize_times else 0
            avg_save = sum(save_times) / len(save_times) if save_times else 0
            print(f"[{time.strftime('%H:%M:%S')}] Среднее время ответа: {avg_time:.2f} сек (summarize: {avg_summarize:.2f} сек, save_summaries: {avg_save:.2f} сек)")
        return successful, failed
 
    def run(self):
        consecutive_failures = 0
        while self.is_running and self.current_rate <= self.max_rate:
            print(f"\n{'='*60}")
            print(f"Текущая интенсивность: {self.current_rate} запросов в секунду")
            successful, failed = self.run_phase(self.current_rate)
            failure_ratio = failed / (successful + failed) if (successful + failed) > 0 else 1
            if failure_ratio > 0.7:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print("Сервер перестал отвечать!")
                    break
            else:
                consecutive_failures = 0
            self.current_rate += self.step
            time.sleep(max(1, 5 - (self.current_rate / 20)))
                    print(f"\nМаксимальная достигнутая интенсивность: {min(self.current_rate, self.max_rate)} запр/сек")

def main():
    BASE_URL = "http://localhost:8000"
    try:
        tester = LoadTester(base_url=BASE_URL, start_rate=1, max_rate=30, step=2, timeout=3)
        tester.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()
