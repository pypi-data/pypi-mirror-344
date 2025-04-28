# latex-generator-itmo-aniciya

**Генератор LaTeX в функциональном стиле**

Проект реализует библиотеку для функциональной генерации LaTeX-документов без использования сторонних пакетов. В рамках задания реализованы:

1. **Функция генерации таблиц**: принимает 2D список (список строк), возвращает строку с валидным LaTeX-кодом таблицы.
2. **Функция генерации изображений**: включает указанное изображение в LaTeX-шаблон.
3. **Пример использования**: отдельный скрипт собирает документ, используя обе функции, и сохраняет `.tex` файл для дальнейшей компиляции (например, в Overleaf).

---

## Возможности

- Генерация таблиц с автоматическим выравниванием и заполнением пустых ячеек
- Вставка изображений в документ LaTeX
- Пакетировка в библиотеку с помощью Poetry
- Тестирование с использованием pytest

---

## Требования

- Python 3.9+
- Poetry для сборки и управления зависимостями

---

## Установка

Установить из PyPI/TestPyPI (после публикации):

```bash
pip install latex-generator-itmo-aniciya
```

Или локально из исходников:

```bash
git clone https://github.com/aniciya777/latex-generator-itmo-aniciya.git
cd latex-generator-itmo-aniciya
poetry install
poetry build
pip install dist/latex_generator_itmo_aniciya-0.2.0-py3-none-any.whl
```

---

## Использование

```python
from latex_generator_itmo_aniciya import generate_table, generate_image

table = [
    ['Version', 'Latest micro version', 'Release Date', 'End of full support', 'End of security fixes'],
    ['3.9',     '3.9.22',   '2020-10-05',   '2022-05-17',   '2025-10'],
    ['3.10',    '3.10.17',  '2021-10-04',   '2023-04-05',   '2026-10'],
    ['3.11',    '3.11.12',  '2022-10-24',   '2024-04-02',   '2027-10'],
    ['3.12',    '3.12.10',  '2023-10-02',   '2025-04-08',   '2028-10'],
    ['3.13',    '3.13.3',   '2024-10-0',    '2026-05',      '2029-10'],
    ['3.14',    '3.14.0a7', '2025-10-07',   '2027-05',      '2030-10'],
]

with open('output.tex', 'w', encoding="utf-8") as file:
    print(generate_table(table), file=file)
print("Сохранён файл output.tex")
```

Скомпилировать результат можно, например, командой:

```bash
pdflatex output.tex
```

---

## Тестирование

Для запуска тестов используется `pytest`:

```bash
poetry run pytest
```

## Лицензия

MIT © aniciya777
