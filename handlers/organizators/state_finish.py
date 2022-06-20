import aiogram.dispatcher
from aiogram.types import CallbackQuery

from keyboards.inline.state_finish import state_finish_callback
from loader import dp
from utils.bot_utils import delete_last_message_call


@dp.callback_query_handler(state_finish_callback.filter(), state='*')
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: aiogram.dispatcher.FSMContext):
    await delete_last_message_call(call)
    await state.finish()
