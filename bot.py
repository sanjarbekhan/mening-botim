import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums import ChatMemberStatus, ParseMode
from aiogram.client.default import DefaultBotProperties

# ==========================================
# SOZLAMALAR
# ==========================================
API_TOKEN = "8409047534:AAH0h-FogMveHfKuqwkNLyW_4JXk8jp3c54"
@dp.message(Form.phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    check_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="✅ Obunani tekshirish")]], resize_keyboard=True)
    
    # Barcha ijtimoiy tarmoqlar havolalari
    text = (
        "<b>Ishtirok etish uchun quyidagi sahifalarimizga obuna bo'ling:</b>\n\n"
        "1. YouTube: https://www.youtube.com/@bolalartashkiloti\n"
        "2. Facebook: [https://www.facebook.com/kamalakbt.uz]\n"
        "3. Instagram: [https://www.instagram.com/bolalartashkiloti?igsh=b3l0bGJheHA4NGJo]\n"
        "4. Telegram: https://t.me/bolalartashkilotiuz\n\n"
        "<i>Eslatma:Iltimos barcha kanallarga obuna bo'ling!</i>"
    )
    
    await message.answer(text, reply_markup=check_kb, disable_web_page_preview=True)
    await state.set_state(Form.check_sub)
ADMIN_ID = 6755433894

# ==========================================
# TEST SAVOLLARI
# ==========================================
QUIZ_DATA = [
    {"q": "1. \"Bolalar harakati\" sardorlar saylovi har o‘quv yilida necha bosqichda o‘tkaziladi?", "o": ["A) 5", "B) 4", "C) 3", "D) 2"], "a": "B) 4"},
    {"q": "2. \"Ustoz AI\" yo‘nalishi sardorining vazifasi nima?", "o": ["A) Bolalarni kasb-hunarga, qolaversa, zamonaviy kasblarni o‘rganishga bo‘lgan qiziqishlarini qo‘llab-quvvatlash", "B) Bolalarning tillarga bo‘lgan qiziqishlarini oshirish", "C) Bolalar o‘rtasida kitobxonlik madaniyatini oshirish", "D) Bolalarning iqtidorini qo‘llab-quvvatlash"], "a": "A) Bolalarni kasb-hunarga, qolaversa, zamonaviy kasblarni o‘rganishga bo‘lgan qiziqishlarini qo‘llab-quvvatlash"},
    {"q": "3. O‘zbekiston bolalar tashkiloti Boshqaruv Kengashi raisi kim?", "o": ["A) Husnora Axadova", "B) Ruxsora Shokirova", "C) Hasanboy Nabiyev", "D) Surayyo Rahmonova"], "a": "C) Hasanboy Nabiyev"},
    {"q": "4. \"Jasorat\" yo‘nalishi sardorining asosiy vazifasi nimadan iborat?", "o": ["A) Bolalarni Vatanga muhabbat, milliy va umuminsoniy qadriyatlarga hurmat ruhida tarbiyalashga ko‘maklashish", "B) Bolalarning media savodxonligini oshirish va media yo‘nalishiga qiziqishi bor bolalarni qo‘llab-quvvatlash", "C) Yosh ijodkor bolalarni qo‘llab-quvvatlash va mushoira klublarini tashkil etish", "D) Xayriya tadbirlarini va aksiyalarni tashkil etish"], "a": "A) Bolalarni Vatanga muhabbat, milliy va umuminsoniy qadriyatlarga hurmat ruhida tarbiyalashga ko‘maklashish"},
    {"q": "5. O‘zbekistonda Bola huquqlari bo‘yicha vakil (Bolalar ombudsmani) kim?", "o": ["A) Aliya Yunusova", "B) Surayyo Rahmonova", "C) Hasanboy Nabiyev", "D) Dilshodbek Rahimov"], "a": "B) Surayyo Rahmonova"},
    {"q": "6. Risolat buvining Rustam ismli nevarasi, Momiq laqabli mushugi va Qoplon laqabli iti bor. Buvining nechta nevarasi bor?", "o": ["A) 3", "B) 2", "C) 4", "D) 1"], "a": "D) 1"},
    {"q": "7. Karim maktabga boradigan yo‘lga 10 daqiqa sarflaydi. Agar u do‘sti bilan boradigan bo‘lsa, qancha vaqt sarflaydi?", "o": ["A) 7 daqiqa", "B) 15 daqiqa", "C) 10 daqiqa", "D) To‘g‘ri javob yo‘q"], "a": "C) 10 daqiqa"},
    {"q": "8. Bog‘da 8 ta o‘rindiq bor edi. Uchtasi bo‘yaldi. Bog‘da nechta o‘rindiq bo‘ldi?", "o": ["A) 8", "B) 7", "C) 9", "D) 5"], "a": "A) 8"},
    {"q": "9. “Buvamning oshqozonidagi mamlakat” bolalar kitobining muallifi kim?", "o": ["A) Qobiljon Shermatov", "B) G‘afur G‘ulom", "C) Anvar Obidjon", "D) Sa’dulla Quronov"], "a": "A) Qobiljon Shermatov"},
    {"q": "10. Bolalarga fizika va astronomiya fanlariga qiziqishga yordam beradigan “Koinot javohiri” kitobini kim yozgan?", "o": ["A) Oybek", "B) Sa’dulla Quronov", "C) Abdulla Oripov", "D) Mirzo Ulug‘bek"], "a": "B) Sa’dulla Quronov"},
    {"q": "11. She’riy shaklda yozilgan, mehr, tabiat va ota-onaga hurmat haqida ta’sirli asar \"Bola va Quyosh\" muallifi kim?", "o": ["A) Alisher Navoiy", "B) Erkin Vohidov", "C) G‘afur G‘ulom", "D) Xudoyberdi To‘xtaboyev"], "a": "B) Erkin Vohidov"},
    {"q": "12. Termometr 15 darajani ko‘rsatmoqda. Ikkita shunday termometr necha darajani ko‘rsatadi?", "o": ["A) 15 darajani", "B) 30 darajani", "C) 45 darajani", "D) 60 darajani"], "a": "A) 15 darajani"},
    {"q": "13. Nimani tayyorlash mumkin, lekin yeb bo‘lmaydi?", "o": ["A) Muzqaymoq", "B) Tez tayyorlanadigan ovqatlar", "C) Darslar (uy vazifasi)", "D) Mevalar"], "a": "C) Darslar (uy vazifasi)"},
    {"q": "14. Nima doim ko‘payib boraveradi, lekin hech qachon kamaymaydi?", "o": ["A) Tabassum", "B) Insonning yoshi", "C) Vaqt", "D) Soniya"], "a": "B) Insonning yoshi"},
    {"q": "15. O‘zbekiston Bolalar Tashkilotida nechta yo‘nalish bor?", "o": ["A) 7", "B) 9", "C) 6", "D) 10"], "a": "B) 9"},
]

# ==========================================
# FSM (HOLATLAR)
# ==========================================
class Form(StatesGroup):
    name = State()
    surname = State()
    age = State()
    phone = State()
    check_sub = State()
    quiz = State()

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
finished_users = set()

# ==========================================
# HANDLERLAR
# ==========================================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id in finished_users:
        await message.answer("Siz testni topshirib bo'lgansiz.")
        return
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Tanlovda ishtirok etish")]], resize_keyboard=True)
    await message.answer(f"Salom {message.from_user.first_name}!", reply_markup=kb)

@dp.message(F.text == "Tanlovda ishtirok etish")
async def process_start(message: types.Message, state: FSMContext):
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
    await state.update_data(age=message.text)
    phone_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]], resize_keyboard=True)
    await message.answer("Telefon raqamingizni yuboring (Tugmani bosing):", reply_markup=phone_kb)
    await state.set_state(Form.phone)

@dp.message(Form.phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    check_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="✅ Obunani tekshirish")]], resize_keyboard=True)
    text = "Ishtirok etish uchun quyidagi kanallarga obuna bo'ling:\n\n" + "\n".join(CHANNELS)
    await message.answer(text, reply_markup=check_kb)
    await state.set_state(Form.check_sub)

@dp.message(Form.check_sub, F.text=="✅ Obunani tekshirish")
async def check_sub_logic(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    not_subbed = []
    
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                not_subbed.append(channel)
        except Exception:
            not_subbed.append(channel)
            
    if not not_subbed:
        go_quiz_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🚀 Testni boshlash")]], resize_keyboard=True)
        await message.answer("Raxmat! Obuna tasdiqlandi. Testni boshlashingiz mumkin.", reply_markup=go_quiz_kb)
    else:
        text = "Siz hali hamma kanallarga obuna bo'lmadingiz. Iltimos obuna bo'lib qaytadan tekshiring:\n\n" + "\n".join(not_subbed)
        await message.answer(text)

@dp.message(F.text == "🚀 Testni boshlash")
async def start_quiz_logic(message: types.Message, state: FSMContext):
    await state.update_data(score=0, current_q=0, start_time=datetime.now().timestamp())
    await send_quiz_question(message, state)

async def send_quiz_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data.get('current_q', 0)
    
    if q_idx >= len(QUIZ_DATA):
        await finish_quiz_logic(message, state)
        return
        
    question = QUIZ_DATA[q_idx]
    opts = [[KeyboardButton(text=opt)] for opt in question['o']]
    kb = ReplyKeyboardMarkup(keyboard=opts, resize_keyboard=True)
    await message.answer(f"Savol {q_idx+1}:\n\n{question['q']}", reply_markup=kb)
    await state.set_state(Form.quiz)

@dp.message(Form.quiz)
async def handle_quiz_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data.get('current_q', 0)
    score = data.get('score', 0)
    
    if message.text == QUIZ_DATA[q_idx]['a']:
        score += 1
        
    await state.update_data(score=score, current_q=q_idx + 1)
    await send_quiz_question(message, state)

async def finish_quiz_logic(message: types.Message, state: FSMContext):
    data = await state.get_data()
    finished_users.add(message.from_user.id)
    score = data.get('score', 0)
    start_time = data.get('start_time')
    time_taken = datetime.now().timestamp() - start_time
    
    await message.answer(f"Tabriklaymiz! Test tugadi.\nSiz {len(QUIZ_DATA)} tadan {score} ta to'g'ri javob berdingiz.", reply_markup=ReplyKeyboardRemove())
    
    report = (f"🔔 YANGI NATIJA:\n👤 {data['name']} {data['surname']}\n📞 {data['phone']}\n"
              f"📅 Yosh: {data['age']}\n📊 Ball: {score}/15\n⏱ Vaqt: {time_taken:.1f}s")
    
    try:
        await bot.send_message(ADMIN_ID, report)
    except Exception as e:
        logging.error(f"Adminga xabar yuborishda xato: {e}")
        
    await state.clear()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
