import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums import ChatMemberStatus

# --- SOZLAMALAR ---
API_TOKEN = "8409047534:AAG0CBuYEeYMt7_cmXlDyeVEZ5L09LcVt3s"
CHANNELS = ["@bolalartashkilotiuz", "@xasanboy_nabiyev"] # @ belgisi bilan yozing
ADMIN_ID = 6755433894 # O'zingizning ID raqamingiz

# --- TEST SAVOLLARI ---
QUIZ_DATA = [
    {"q": "1. Oʻzbekiston Bolalar Tashkiloti qachon tashkil etilgan?", "o": ["A) 2024-yil 16-aprel", "B) 2023-yil 1-mart", "C) 2025-yil 10-yanvar", "D) 2022-yil 5-may"], "a": "A) 2024-yil 16-aprel"},
    {"q": "2. Bolalar tashkilotiga aʼzo boʻlish yoshi nechi yoshdan boshlanadi?", "o": ["A) 8 yoshdan", "B) 10 yoshdan", "C) 12 yoshdan", "D) 14 yoshdan"], "a": "B) 10 yoshdan"},
    {"q": "3. Bosh sardorning vazifasi nimadan iborat?", "o": ["A) Moliyaviy hisobotlar", "B) Faoliyatni yakunlash", "C) Sardorlar faoliyatini muvofiqlashtirish", "D) Xalqaro aloqalar"], "a": "C) Sardorlar faoliyatini muvofiqlashtirish"},
    {"q": "4. Oʻzbekiston Bolalar Tashkilotida nechta yo’nalish bor?", "o": ["A) 5 ta", "B) 7 ta", "C) 9 ta", "D) 11 ta"], "a": "C) 9 ta"},
    {"q": "5. Tashkilotning to‘liq nomi qanday?", "o": ["A) Oʻzbekiston Yoshlar Jamiyati", "B) Oʻzbekiston Bolalar Tashkiloti", "C) Bolalar va Oila Markazi", "D) Respublika Forum"], "a": "B) Oʻzbekiston Bolalar Tashkiloti"},
    {"q": "6. Tashkilot nomi ingliz tilida qanday nomlanadi?", "o": ["A) Non-governmental non-profit organization “Children's Organization of Uzbekistan”", "B) Governmental organization “Children’s Uzbekistan”", "C) Private charity", "D) International union"], "a": "A) Non-governmental non-profit organization “Children's Organization of Uzbekistan”"},
    {"q": "7. Tashkilotning rahbar organi qayerda joylashgan?", "o": ["A) Toshkent sh., Navoiy ko‘chasi, 11A uy", "B) Mustaqillik maydoni", "C) Eski shahar", "D) Toshkent viloyati"], "a": "A) Toshkent sh., Navoiy ko‘chasi, 11A uy"},
    {"q": "8. Loyiha nima?", "o": ["A) Maʼlum bir maqsadga erishish uchun tartiblangan faoliyatlar majmui", "B) Faqat hujjat yozish", "C) Ichki yig'ilish"], "a": "A) Maʼlum bir maqsadga erishish uchun tartiblangan faoliyatlar majmui"},
    {"q": "9. Yashil makon sardorining vazifasi?", "o": ["A) Sport tadbirlari", "B) Ekologik madaniyatni targ‘ib qilish", "C) Moliyaviy hisoblar", "D) San'at tanlovlari"], "a": "B) Ekologik madaniyatni targ‘ib qilish"},
    {"q": "10. Nazorat-taftish komissiyasi qanday organ?", "o": ["A) Tadbir guruhi", "B) Moliyaviy‑xo‘jalik nazorati", "C) Marketing bo'limi", "D) Kengash"], "a": "B) Moliyaviy‑xo‘jalik nazorati"},
    {"q": "11. Tashkilotning asosiy maqsadi?", "o": ["A) Daromad olish", "B) Bolalar huquqlarini himoya qilish", "C) Faqat sport", "D) Tashqi siyosat"], "a": "B) Bolalar huquqlarini himoya qilish"},
    {"q": "12. Tashkilot aʼzolari nimani amalga oshiradilar?", "o": ["A) Faqat loyihalar", "B) Loyihalar, aksiyalar, treninglarda ishtirok etadilar", "C) Kitob nashr qilish"], "a": "B) Loyihalar, aksiyalar, treninglarda ishtirok etadilar"},
    {"q": "13. Tashkilot qaysi shaklda tashkil etilgan?", "o": ["A) Davlat organi", "B) Nodavlat, notijorat tashkilot", "C) Xususiy korxona", "D) Xalqaro"], "a": "B) Nodavlat, notijorat tashkilot"},
    {"q": "14. Plogging aksiya maqsadi nima?", "o": ["A) Pul yig‘ish", "B) Atrof-muhitni tozalash va sog'lom turmush", "C) Reyting", "D) Sport"], "a": "B) Atrof-muhitni tozalash va sog'lom turmush"},
    {"q": "15. Butunjahon bolalar kuni qachon?", "o": ["A) 1-iyun", "B) 20-noyabr", "C) 11-oktabr", "D) 1-sentabr"], "a": "B) 20-noyabr"},
]

# --- FSM HOLATLARI ---
class Form(StatesGroup):
    name = State()
    surname = State()
    age = State()
    check_sub = State()
    quiz = State()
    bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
finished_users = set() # Bir marta ishlaganlarni saqlash

# --- KEYBOARDS ---
def get_quiz_kb(options):
    kb = [[KeyboardButton(text=opt)] for opt in options]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Tanlovda ishtirok etish")]], resize_keyboard=True)
check_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="✅ Obunani tekshirish")]], resize_keyboard=True)
go_quiz_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🚀 Testni boshlash")]], resize_keyboard=True)
# --- HANDLERS ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id in finished_users:
        await message.answer("Siz testni topshirib bo'lgansiz, qayta topshirish mumkin emas.")
        return
    await message.answer(f"Salom {message.from_user.first_name}, tanlovga xush kelibsiz! Tanlovda ishtirok etmoqchimisiz?", reply_markup=start_kb)
@dp.message(F.text == "Tanlovda ishtirok etish")
async def process_start_contest(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.name)
@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(Form.surname)
@dp.message(Form.surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(Form.age)
@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, yoshingizni son bilan kiriting:")
        return
    
    age = int(message.text)
    if age > 18:
        await message.answer("Tanlov 18 yoshgacha bolalar uchun mo'ljallangan.")
        await state.clear()
    else:
        text = "Tanlovda ishtirok etish uchun quyidagi kanallarga obuna bo'ling:\n"
        for ch in CHANNELS: text += f"{ch}\n"
        await message.answer(text, reply_markup=check_kb)
        await state.set_state(Form.check_sub)
# --- O'ZGARTIRILGAN QISM: OBUNA TEKSHIRISH ---
@dp.message(Form.check_sub, F.text=="✅ Obunani tekshirish")
async def check_subscription(message: types.Message, state: FSMContext):
not_subscribed = [] # Obuna bo'lmagan kanallar ro'yxati
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, message.from_user.id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                not_subscribed.append(ch)
        except Exception as e:
            # Agar bot kanal admini bo'lmasa yoki kanal topilmasa, xatolik bermaslik uchun
            logging.error(f"Xatolik: {ch} - {e}")
            not_subscribed.append(ch)

    if not not_subscribed: # Agar ro'yxat bo'sh bo'lsa (demak hamma kanalga a'zo)
        await message.answer("Obuna tasdiqlandi! Testni boshlashga tayyormisiz?", reply_markup=go_quiz_kb)
    else:
        # Obuna bo'lmagan kanallarni qayta chiqarib beramiz
text = "❌ <b>Siz hali kanallarga obuna bo'lmadingiz!</b>\n\nIltimos, quyidagilarga obuna bo'lib, qayta tekshiring:\n"
for ch in not_subscribed:
text += f"👉 {ch}\n"
await message.answer(text, parse_mode="HTML", reply_markup=check_kb)
@dp.message(F.text == "🚀 Testni boshlash")
async def start_quiz(message: types.Message, state: FSMContext):
    # Qo'shimcha xavfsizlik: Test boshlashdan oldin ham yana bir bor tekshirish
    # (Agar xohlasangiz bu qismni olib tashlashingiz mumkin, lekin tavsiya etiladi)
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, message.from_user.id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                 await message.answer("Siz hali hamma kanallarga obuna bo'lmadingiz!", reply_markup=check_kb)
                 return
        except:
            pass

    await state.update_data(score=0, current_q=0)
    await send_question(message, state)

async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data['current_q']
    
    if q_idx >= len(QUIZ_DATA):
        await finish_quiz(message, state)
        return

    question = QUIZ_DATA[q_idx]
    msg = await message.answer(f"⏳ 20 soniya vaqt beriladi!\n\n{question['q']}", reply_markup=get_quiz_kb(question['o']))
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(Form.quiz)
    
    # 20 soniya taymer
    await asyncio.sleep(20)
    
    # Taymerdan keyin holatni tekshirish
    current_state = await state.get_state()
    new_data = await state.get_data()
    
    # Agar foydalanuvchi hali ham shu savolda turgan bo'lsa (javob bermagan bo'lsa)
    if current_state == Form.quiz and new_data.get('current_q') == q_idx:
        await message.answer("⏰ Vaqt tugadi! Keyingi savolga o'tamiz.")
        await state.update_data(current_q=q_idx + 1)
        await send_question(message, state)
@dp.message(Form.quiz)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data['current_q']
    question = QUIZ_DATA[q_idx]
    
    score = data.get('score', 0)
    if message.text == question['a']:
        score += 1
        await message.answer("✅ To'g'ri!")
    else:
        await message.answer(f"❌ Noto'g'ri! To'g'ri javob: {question['a']}")
    
    await state.update_data(score=score, current_q=q_idx + 1)
    await send_question(message, state)

async def finish_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    finished_users.add(message.from_user.id)
    await message.answer(f"Tabriklaymiz {data['name']}! Test tugadi.\nNatijangiz: {data['score']}/{len(QUIZ_DATA)}", reply_markup=ReplyKeyboardRemove())
    
    # Adminga hisobot yuborish
    report = f"Yangi natija:\nIsm: {data['name']}\nFamiliya: {data['surname']}\nYosh: {data['age']}\nNatija: {data['score']}"
    await bot.send_message(ADMIN_ID, report)
    await state.clear()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
