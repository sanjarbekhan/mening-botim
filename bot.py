import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums import ChatMemberStatus
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# --- SOZLAMALAR ---
API_TOKEN = "8409047534:AAG0CBuYEeYMt7_cmXlDyeVEZ5L09LcVt3s"
CHANNELS = ["https://www.youtube.com/@Uzyoshlaryetakchilari", "https://www.instagram.com/uzyoshlaryetakchilari/", "https://www.facebook.com/profile.php?id=100083056130781", "@uzyoshlaryetakchilarii"]
ADMIN_ID = 6755433894

# --- TEST SAVOLLARI ---
# --- YANGILANGAN TEST SAVOLLARI (SIZNING KALITINGIZ BO'YICHA) ---
QUIZ_DATA = [
    {"q": "1. \"Bolalar harakati\" sardorlar saylovi har o‘quv yilida necha bosqichda o‘tkaziladi?", "o": ["A) 5", "B) 4", "C) 3", "D) 2"], "a": "B) 4"},
    {"q": "2. \"Ustoz AI\" yo‘nalishi sardorining vazifasi nima?", "o": ["A) Bolalarni kasb-hunarga, qolaversa, zamonaviy kasblarni o‘rganishga bo‘lgan qiziqishlarini qo‘llab-quvvatlash", "B) Bolalarning tillarga bo‘lgan qiziqishlarini oshirish", "C) Bolalar o‘rtasida kitobxonlik madaniyatini oshirish", "D) Bolalarning iqtidorini qo‘llab-quvvatlash"], "a": "A) Bolalarni kasb-hunarga, qolaversa, zamonaviy kasblarni o‘rganishga bo‘lgan qiziqishlarini qo‘llab-quvvatlash"},
    {"q": "3. O‘zbekiston bolalar tashkiloti Boshqaruv Kengashi raisi kim?", "o": ["A) Husnora Axadova", "B) Ruxsora Shokirova", "C) Hasanboy Nabiyev", "D) Alisher Sa’dullayev"], "a": "C) Hasanboy Nabiyev"},
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
] # --- FSM HOLATLARI ---
class Form(StatesGroup):
    name = State()
    surname = State()
    age = State()
    phone = State()  # Yangi holat
    check_sub = State()
    quiz = State()

def get_phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

finished_users = set() # Bir marta ishlaganlarni saqlash
all_results = [] # Barcha natijalarni vaqt bilan saqlab borish uchun

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
        await state.update_data(age=age)
        await message.answer("Raxmat! Endi pastdagi tugmani bosib telefon raqamingizni yuboring:", 
                             reply_markup=get_phone_kb())
        await state.set_state(Form.phone)

async def check_subscription(message: types.Message, state: FSMContext):
    not_subscribed = []
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, message.from_user.id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                not_subscribed.append(ch)
        except Exception as e:
            logging.error(f"Xatolik: {ch} - {e}")
            not_subscribed.append(ch)

    if not not_subscribed:
        await message.answer("Obuna tasdiqlandi! Testni boshlashga tayyormisiz?", reply_markup=go_quiz_kb)
    else:
        text = "❌ <b>Siz hali kanallarga obuna bo'lmadingiz!</b>\n\nIltimos, quyidagilarga obuna bo'lib, qayta tekshiring:\n"
        for ch in not_subscribed:
            text += f"👉 {ch}\n"
        await message.answer(text, reply_markup=check_kb)

@dp.message(F.text == "🚀 Testni boshlash")
async def start_quiz(message: types.Message, state: FSMContext):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, message.from_user.id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                 await message.answer("Siz hali hamma kanallarga obuna bo'lmadingiz!", reply_markup=check_kb)
                 return
        except:
            pass

    await state.update_data(score=0, current_q=0, start_time=datetime.now().timestamp())
    await send_question(message, state)

async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data.get('current_q', 0)
    
    if q_idx >= len(QUIZ_DATA):
        await finish_quiz(message, state)
        return

    question = QUIZ_DATA[q_idx]
    msg = await message.answer(f"⏳ 20 soniya vaqt beriladi!\n\n{question['q']}", reply_markup=get_quiz_kb(question['o']))
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(Form.quiz)
    
    await asyncio.sleep(20)
    
    current_state = await state.get_state()
    new_data = await state.get_data()
    
    if current_state == Form.quiz.state and new_data.get('current_q') == q_idx:
        await message.answer("⏰ Vaqt tugadi! Keyingi savolga o'tamiz.")
        await state.update_data(current_q=q_idx + 1)
        await send_question(message, state) 
@dp.message(Form.quiz)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_idx = data.get('current_q', 0)
    
    if q_idx >= len(QUIZ_DATA):
        return

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
    
    name = data.get('name', 'Ishtirokchi')
    surname = data.get('surname', '')
    age = data.get('age', 'Noma\'lum')
    score = data.get('score', 0)
    
    start_time = data.get('start_time', datetime.now().timestamp())
    end_time = datetime.now().timestamp()
    time_taken = end_time - start_time
    
    all_results.append({
        'name': name,
        'surname': surname,
        'age': age,
        'score': score,
        'time_taken': time_taken
    })

    await message.answer(f"Tabriklaymiz {name}! Test tugadi.\nNatijangiz: {score}/{len(QUIZ_DATA)}\nSarflangan vaqt: {time_taken:.1f} soniya", reply_markup=ReplyKeyboardRemove())
    
    report = f"🔔 <b>Yangi natija:</b>\n👤 Ism: {name} {surname}\n📅 Yosh: {age}\n📊 Natija: {score}/{len(QUIZ_DATA)}\n⏱ Vaqt: {time_taken:.1f} sekund"
    try:
        await bot.send_message(ADMIN_ID, report)
    except Exception as e:
        logging.error(f"Adminga xabar yuborishda xatolik: {e}")
        
    await state.clear()

@dp.message(Command("natijalar"))
async def get_all_results(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return 
        
    if not all_results:
        await message.answer("Hozircha hech kim testni ishlamadi.")
        return
        
    sorted_results = sorted(all_results, key=lambda x: (-x['score'], x['time_taken']))
    
    text = "🏆 <b>UMUMIY REYTING:</b>\n\n"
    for i, res in enumerate(sorted_results, 1):
        text += f"<b>{i}-o'rin:</b> {res['name']} {res['surname']} | {res['score']} ball | ⏱ {res['time_taken']:.1f} sek\n"
        
    await message.answer(text[:4000])

async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
