from threading import Thread
from collections import Counter
import matplotlib.pyplot as plt
import requests
import re

# Загрузка текста по url
def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Обработка текста Mapper
def map_words(text, result, index):
    words = re.findall(r'\b\w+\b', text.lower())
    result[index] = Counter(words)

# Объединение результатов Reducer
def reduce_counts(counters):
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter

# Визуализация результатов
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.barh(words, counts)
    plt.xlabel("Частота")
    plt.ylabel("Слова")
    plt.title(f"Топ самых частых слов")
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    url = input("Введите URL для получения текста: ")

    try:
        text = fetch_text(url)

        # Разбиваем текст на части для многопоточности
        chunk_size = len(text) // 4
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        threads = []
        results = [None] * len(chunks)

        # Создаем и запускаем потоки
        for i, chunk in enumerate(chunks):
            thread = Thread(target=map_words, args=(chunk, results, i))
            threads.append(thread)
            thread.start()

        # Ожидаем завершения всех потоков
        for thread in threads:
            thread.join()

        word_counts = reduce_counts(results)
        visualize_top_words(word_counts, top_n=10)

    except Exception as e:
        print(f"Ошибка: {e}")
