from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("student_keyboard", "Клавиатура ученика"),
            types.BotCommand("teacher_keyboard", "Клавиатура учителя"),
            types.BotCommand("organizators_keyboard", "Клавиатура организатора"),

        ]
    )
