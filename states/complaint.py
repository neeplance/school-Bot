from aiogram.dispatcher.filters.state import StatesGroup, State


class Complaint(StatesGroup):
    complaint = State()