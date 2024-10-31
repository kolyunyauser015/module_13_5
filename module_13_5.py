from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.add(button_1)
kb.insert(button_2)


@dp.message_handler(text="Привет!")
async def all_message(messange):
    await messange.answer("Введите команду /start, чтобы начать общение.")


@dp.message_handler(commands=['start'])
async def start(messange):
    await messange.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def set_age(messange):
    await messange.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(messange, state):
    await state.update_data(first=messange.text)
    await messange.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(messange, state):
    await state.update_data(second=messange.text)
    await messange.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_colories(messange, state):
    await state.update_data(third=messange.text)
    data = await state.get_data()
    calc_colories = 10 * int(data['first']) + 6.25 * int(data['second']) + 5 * int(data['third'] + 5)
    await messange.answer(f"Ваша норма калорий: {calc_colories}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
