from argparse import ArgumentParser
from pathlib import Path
import asyncio
import shutil
import os

""" 
Пример команды запуска
python3 task_1.py "/Volumes/Data/Секретно" "/Volumes/Data/Секретно/SORTED"
"""

async def read_folder(source_folder: Path, output_folder: Path):
    """ Читаем рекурсивно файлы в папке """
    try:
        for root, _, files in os.walk(source_folder):
            root_path = Path(root)
            tasks = []
            for file in files:
                file_path = root_path / file
                tasks.append(copy_file(file_path, output_folder))
            await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Ошибка чтения папки: {e}")

async def copy_file(file_path: Path, output_folder: Path):
    """ Копируем файл в папку соответстующую расширению файла."""
    try:
        ext = file_path.suffix[1:]  # Получаем расширение
        if not ext:
            ext = "unknown"

        target_folder = output_folder / ext
        target_folder.mkdir(parents=True, exist_ok=True)

        target_path = target_folder / file_path.name
        shutil.copy2(file_path, target_path)  # Копируем файл
        print(f"Скопировано из {file_path} в {target_path}")
    except Exception as e:
        print(f"Ошибка копирования: {e}")

if __name__ == "__main__":
    # Парсер аргументов
    parser = ArgumentParser(description="Сортировка файлов.")
    parser.add_argument("source_folder", type=str, help="Исходная папка.")
    parser.add_argument("output_folder", type=str, help="Папка назначения.")

    args = parser.parse_args()

    try:
        source_folder = Path(args.source_folder).resolve()
        output_folder = Path(args.output_folder).resolve()

        if not source_folder.is_dir():
            print(f"Папка {source_folder} не существует или это не директория.")
            exit(1)

        # Запуск асинхронной обработки
        asyncio.run(read_folder(source_folder, output_folder))
        print("Сортировка завершена.")
    except Exception as e:
        print(f"Ошибка выполнения сортировки: {e}")
