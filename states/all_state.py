from aiogram.dispatcher.filters.state import StatesGroup, State

class GetTasks(StatesGroup):
    task = State()

class GetSolve(StatesGroup):
    solve = State()

class ShowDocs(StatesGroup):
    doc = State()

class GetDocs(StatesGroup):
    doc = State()

class Test(StatesGroup):
    test = State()

class GetSchedule(StatesGroup):
    schedule = State()

class GetStudents(StatesGroup):
    students = State()

class GetTeachers(StatesGroup):
    teachers = State()

class GetEvent(StatesGroup):
    discipline = State()
    event_name = State()
    event_text = State()
    team = State()

class GetReminder(StatesGroup):
    reminder = State()
    users_type = State()
    date = State()
    time = State()

class Question(StatesGroup):
    question = State()

class SubmitTasks(StatesGroup):
    auditory = State()
    discipline = State()
    number_of_tasks = State()

class PutRate(StatesGroup):
    name = State()
    discipline = State()
    task = State()
    rate = State()

class GetRate(StatesGroup):
    name = State()
    discipline = State()
    task = State()
    rate = State()

class GetMyRate(StatesGroup):
    rate = State()
class GetAllRate(StatesGroup):
    rate = State()

