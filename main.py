import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '8019941554:AAFG_rUK2RkcBaZ1Osr_O9PlNcPihq8fBvY'
ADMIN_CHAT_ID = 411134984

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

questions = [
    "Опиши максимально подробно тему, откуда куда и что?",
    "Какой апсайд, какой минимум для входа, какой максимум?",
    "Как долго длится сделка?",
    "Какие риски ты видишь?",
    "Расскажи, пробовал ли ты сам. Если да — на какой объём и какой вышел результат, приложи транзакции."
]

class Form(StatesGroup):
    step_0 = State()
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()

user_answers = {}

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.step_0)
    user_answers[message.from_user.id] = []
    await message.answer(questions[0])

@dp.message(Form.step_0)
async def step_0(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_1)
    await message.answer(questions[1])

@dp.message(Form.step_1)
async def step_1(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_2)
    await message.answer(questions[2])

@dp.message(Form.step_2)
async def step_2(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_3)
    await message.answer(questions[3])

@dp.message(Form.step_3)
async def step_3(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_4)
    await message.answer(questions[4])

@dp.message(Form.step_4)
async def step_4(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)

    await message.answer(
        "Отлично, как только мы ознакомимся, мы сразу с тобой свяжемся в любом результате.\n\n"
        "Не спамь пожалуйста, если мы не ответили — значит мы просто не добрались до твоего сообщения. "
        "Обычно пару часов."
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Предложить ещё тему")]],
        resize_keyboard=True
    )
    await message.answer("Хочешь предложить ещё тему?", reply_markup=keyboard)

    user_id = message.from_user.id
    username = message.from_user.username or "без ника"

    summary = "\n\n".join(
        [f"<b>{questions[i]}</b>\n{user_answers[user_id][i]}" for i in range(len(questions))]
    )

    await bot.send_message(
        ADMIN_CHAT_ID,
        f"📩 Заявка от @{username}:\n\n{summary}"
    )

    user_answers.pop(user_id)
    await state.clear()

@dp.message(F.text.lower() == "предложить ещё тему")
async def restart(message: Message, state: FSMContext):
    await cmd_start(message, state)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
