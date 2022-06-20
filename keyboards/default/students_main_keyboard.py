from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

students_main_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Решить тест'),
            KeyboardButton(text='Решить задачу')
        ],[
            KeyboardButton(text='Мои оценки'),
            KeyboardButton(text='Мои решения')
        ],
        [
            KeyboardButton(text='Мероприятия')
        ],
        [
            KeyboardButton(text='Получить расписание')
        ],
        [
            KeyboardButton(text='Вопрос преподавателю')
        ],
        [
            KeyboardButton(text='Сдать работу')
        ],
        [
            KeyboardButton(text='Загрузить документы')
        ],
        [
            KeyboardButton(text='Оставить отзыв'),
            KeyboardButton(text='Оставить жалобу')
        ],
    ],
    resize_keyboard=True
)