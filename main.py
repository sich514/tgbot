import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '7853348507:AAHoebNIo8lXep2hZ-wJhYgN7dahXzXAGP4'
ADMIN_CHAT_ID = 411134984

# ⚙️ Инициализация бота
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

questions = [
    "🧠 Опиши максимально подробно тему, откуда, куда и что?",
    "📈 Какой апсайд, какой минимум для входа, какой максимум?",
    "⏳ Как долго длится сделка?",
    "⚠️ Какие риски ты видишь?",
    "📊 Расскажи, пробовал ли ты сам. Если да — на какой объём и какой вышел результат, приложи транзакции."
]

class Form(StatesGroup):
    step_0 = State()
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()

user_answers = {}

# 👋 Приветствие
@dp.message(Command("start"))
async def welcome(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Начать заявку")]],
        resize_keyboard=True
    )

    await message.answer(
        "<b>У тебя есть идея как заработать, но нет капитала?</b>\n\n"
        "Опиши свою идею максимально подробно. Если нам понравится — мы поделимся с тобой профитом с этой сделки.\n\n"
        "Нажми кнопку ниже, чтобы начать 👇",
        reply_markup=keyboard
    )

# 🟢 Запуск формы по кнопке
@dp.message(F.text == "🚀 Начать заявку")
async def start_form(message: Message, state: FSMContext):
    await state.set_state(Form.step_0)
    user_answers[message.from_user.id] = []
    await message.answer(questions[0])

# ✅ Обработка шагов анкеты
@dp.message(Form.step_0)
async def handle_step_0(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_1)
    await message.answer(questions[1])

@dp.message(Form.step_1)
async def handle_step_1(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_2)
    await message.answer(questions[2])

@dp.message(Form.step_2)
async def handle_step_2(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_3)
    await message.answer(questions[3])

@dp.message(Form.step_3)
async def handle_step_3(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.set_state(Form.step_4)
    await message.answer(questions[4])

@dp.message(Form.step_4)
async def handle_step_4(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_answers[user_id].append(message.text)

    # 📮 Сообщение пользователю
    await message.answer(
        "Спасибо за заявку!\n\nМы внимательно изучим твою идею и свяжемся с тобой в любом случае.\n\n"
        "⏱ Обычно на это уходит пару часов. Не дублируй сообщение — мы обязательно дойдём."
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="➕ Предложить ещё идею")]],
        resize_keyboard=True
    )
    await message.answer("Хочешь предложить ещё идею?", reply_markup=keyboard)

    # 🧾 Формирование анкеты и отправка админу
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

# 🔄 Повтор подачи заявки
@dp.message(F.text.lower() == "предложить ещё идею")
async def restart_form(message: Message, state: FSMContext):
    await start_form(message, state)

# 🚀 Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
