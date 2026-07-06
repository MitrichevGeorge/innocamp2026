import os
from google import genai

# Указываем прокси через переменные окружения для текущего процесса
# Используем socks5h, чтобы DNS-запросы тоже шли через прокси
os.environ["HTTP_PROXY"] = "socks5h://127.0.0.1:10801"
os.environ["HTTPS_PROXY"] = "socks5h://127.0.0.1:10801"

# Клиент автоматически подхватит эти настройки из окружения


print("Универсальный ИИ-поисковик запущен! (С поддержкой SOCKS5 прокси)\n" + "-" * 50)

while True:
    s = input("\nВведите ваш запрос или вопрос -> ")

    if s.lower() in ['выход', 'exit', 'quit']:
        print("До скорой встречи!")
        break

    if not s.strip():
        continue
        
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=s,
        )
        print("\n[Ответ ИИ]:")
        print(response.text)
        print("-" * 50)

    except Exception as e:
        print(f"\n[Ошибка API]: {e}")
        print("-" * 50)