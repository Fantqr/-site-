import telebot
from telebot import types

API_TOKEN = '7826173334:AAGxfnVCl_naBZKsfsSa9I1chZioTDJVe-Y'
bot = telebot.TeleBot(API_TOKEN)

# Прогресс пользователей
user_progress = {}

# Основное меню
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add('📘 Основы Python', '🌐 Основы сетей', '📊 Алгоритмы')

# Уроки и тесты
lessons = {
    '📘 Основы Python': [
        {
            'lesson': 'Переменные и типы данных.\n\nПример:\nname = "Alice"\nage = 25\nprint(f"Привет, {name}. Тебе {age} лет.")',
            'question': 'Какой тип данных у переменной name?',
            'options': ['str', 'int', 'list'],
            'answer': 'str',
            'theory': '''Переменные в Python — это именованные ссылки на объекты в памяти. Они используются для хранения данных.

Типы данных в Python:
1. `int` — целые числа (1, 2, -5).
2. `float` — числа с плавающей запятой (3.14, -0.001).
3. `str` — строки, последовательности символов ("Hello", "123").
4. `list` — списки, упорядоченные коллекции данных ([1, 2, 3], ["apple", "banana"]).
5. `dict` — словари, хранят пары ключ-значение ({"key": "value"}).

В примере:
```python
name = "Alice"
age = 25
print(f"Привет, {name}. Тебе {age} лет.")
```
Переменная `name` имеет тип данных `str`, так как она хранит строку "Alice".
'''        },
        {
            'lesson': 'Условные операторы.\n\nПример:\nif age > 18:\n    print("Взрослый")\nelse:\n    print("Ребенок")',
            'question': 'Какой оператор используется для альтернативного условия?',
            'options': ['elif', 'else', 'switch'],
            'answer': 'else',
            'theory': '''Условные операторы позволяют программе выполнять разные блоки кода в зависимости от условия.

Основные операторы:
1. `if` — выполняет блок кода, если условие истинно.
2. `else` — выполняется, если условие в `if` ложно.
3. `elif` — проверяет дополнительное условие, если предыдущее ложно.

Пример:
```python
age = 20
if age > 18:
    print("Взрослый")
else:
    print("Ребенок")
```
Здесь, если `age` больше 18, программа напечатает "Взрослый". Если меньше или равно — "Ребенок".
'''        }
    ],
    '🌐 Основы сетей': [
        {
            'lesson': 'IP-адреса и порты.\n\nIP-адрес — это уникальный адрес устройства в сети.',
            'question': 'Какой IP-адрес является локальным?',
            'options': ['8.8.8.8', '172.16.0.1', '192.168.0.1'],
            'answer': '192.168.0.1',
            'theory': '''IP-адрес (Internet Protocol Address) — это уникальный идентификатор устройства в сети.

Типы IP-адресов:
1. Локальные (частные):
   - 192.168.x.x
   - 10.x.x.x
   - 172.16.x.x — 172.31.x.x

2. Публичные — используются для выхода в интернет.

Порт — это числовой идентификатор приложения или службы на устройстве. Например, порт 80 — для HTTP.
'''        }
    ],
    '📊 Алгоритмы': [
        {
            'lesson': 'Бинарный поиск — это алгоритм поиска элемента в отсортированном массиве за логарифмическое время.',
            'question': 'Какое время выполнения у бинарного поиска?',
            'options': ['O(log n)', 'O(n)', 'O(n^2)'],
            'answer': 'O(log n)',
            'theory': '''Бинарный поиск — это алгоритм, который используется для быстрого поиска элемента в **отсортированном** массиве.

Как работает:
1. Делим массив пополам.
2. Сравниваем искомое значение со средней точкой.
3. Если значение меньше — ищем в левой половине, больше — в правой.
4. Повторяем до нахождения элемента или окончания поиска.

Время выполнения — `O(log n)`, так как с каждым шагом область поиска уменьшается в два раза.
'''        }
    ]
}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_progress[message.chat.id] = {section: 0 for section in lessons}
    bot.send_message(message.chat.id, 'Привет! Я IT Shiver Bot. Чем хочешь заняться?', reply_markup=main_menu)

@bot.message_handler(func=lambda message: message.text in lessons)
def send_lesson(message, section=None):
    if message.chat.id not in user_progress:
        user_progress[message.chat.id] = {section: 0 for section in lessons}
    section = section or message.text
    index = user_progress[message.chat.id][section]
    if index < len(lessons[section]):
        lesson_data = lessons[section][index]
        # Добавляем кнопку "Прочитать теорию"
        markup = types.InlineKeyboardMarkup()
        theory_button = types.InlineKeyboardButton(text="📖 Прочитать теорию", callback_data=f"theory_{section}_{index}")
        markup.add(theory_button)
        bot.send_message(message.chat.id, f'Урок:\n\n{lesson_data["lesson"]}', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🏠 В главное меню')
        bot.send_message(message.chat.id, 'Ты прошел все уроки в этом разделе!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('theory_'))
def show_theory(call):
    try:
        _, section, index = call.data.split('_')
        section = str(section)
        index = int(index)

        lesson_data = lessons[section][index]
        bot.send_message(call.message.chat.id, f'Теория:\n\n{lesson_data["theory"]}')

        # После прочтения теории - показать вопрос
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(*lesson_data['options'])
        bot.send_message(call.message.chat.id, f'Вопрос:\n{lesson_data["question"]}', reply_markup=markup)

    except (ValueError, IndexError, KeyError):
        bot.send_message(call.message.chat.id, "Ошибка при загрузке теории.") # Обработка ошибок.

@bot.message_handler(func=lambda message: message.text in sum([x['options'] for x in sum(lessons.values(), [])], []))
def check_answer(message):
    if message.chat.id not in user_progress:
        user_progress[message.chat.id] = {section: 0 for section in lessons}

    # Находим раздел и индекс урока, для которого пользователь выбрал этот ответ
    current_section = None
    current_index = None
    for section in lessons:
        for i, lesson_data in enumerate(lessons[section]):
            if message.text in lesson_data['options']:
                current_section = section
                current_index = i
                break
        if current_section:
            break  # Выходим из внешнего цикла, если раздел найден

    if current_section is not None and current_index is not None:
        correct_answer = lessons[current_section][current_index]['answer']
        if message.text.strip().lower() == correct_answer.strip().lower():
            bot.send_message(message.chat.id, '✅ Правильно! Переходим к следующему уроку.')
            user_progress[message.chat.id][current_section] += 1
            send_lesson(message, current_section)
        else:
            bot.send_message(message.chat.id, '❌ Неправильно, попробуй еще раз.')
    else:
        bot.send_message(message.chat.id, "Похоже, вы еще не выбрали раздел или уже прошли его. Выберите раздел в главном меню.")

@bot.message_handler(func=lambda message: message.text == '🏠 В главное меню')
def back_to_main_menu(message):
    bot.send_message(message.chat.id, 'Чем хочешь заняться?', reply_markup=main_menu)

print('Бот запущен...')
bot.polling(none_stop=True)
