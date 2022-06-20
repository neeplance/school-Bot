from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

organizators_main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать рассылку')
        ],
        [
            KeyboardButton(text='Получить информацию о пользователе')
        ],
        [
            KeyboardButton(text='Мероприятия')
        ],
        [
            KeyboardButton(text='Проверка работ оффлайн')
        ],
        [
            KeyboardButton(text='Добавить расписание'),
            KeyboardButton(text='Получить расписание')
        ],
        [
            KeyboardButton(text='Загрузить документы'),
            KeyboardButton(text='Получить документы')
        ],
        [
            KeyboardButton(text='Просмотр жалоб')
        ],
        [
            KeyboardButton(text='Добавить задачу'),
            KeyboardButton(text='Добавить тест')
        ],
        [
            KeyboardButton(text='Баллы ученика'),
            KeyboardButton(text='Общая успеваемость')
        ],        [
            KeyboardButton(text='Добавить учеников'),
            KeyboardButton(text='Добавить учителей')
        ],
    ],
    resize_keyboard=True
)
