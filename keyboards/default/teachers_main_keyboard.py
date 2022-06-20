from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

teachers_main_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Добавить задачу'),
            KeyboardButton(text='Добавить тест')
        ],
        [
            KeyboardButton(text='Проверить решение задачи')
        ],
        [
            KeyboardButton(text='Получить расписание')
        ],
        [
            KeyboardButton(text='Выставить баллы')
        ],
        [
            KeyboardButton(text='Загрузить документы')
        ],
        [
            KeyboardButton(text='Проверка работ оффлайн')
        ],
        [
            KeyboardButton(text='Баллы ученика'),
            KeyboardButton(text='Общая успеваемость')
        ],
        [
            KeyboardButton(text='Оставить отзыв'),
            KeyboardButton(text='Оставить жалобу')
        ],
    ],
    resize_keyboard=True
)