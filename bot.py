import os
from aiohttp import web
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums import ChatMemberStatus, ParseMode
from aiogram.client.default import DefaultBotProperties

# ==========================================
# SOZLAMALAR
# ==========================================
API_TOKEN = "8409047534:AAGWUpQOIEKeUXED9eRYZGOA454ZYlkXJZg"
ADMIN_ID = 6755433894

# Faqat bot tekshira oladigan Telegram kanallari
CHANNELS = ["@xasanboy_nabiyev", "@bolalartashkilotiuz"] 

# VILOYATLAR RO'YXATI
REGIONS = [
    "Toshkent sh.", "Toshkent vil.", "Andijon", "Farg'ona", "Namangan",
    "Buxoro", "Navoiy", "Jizzax", "Sirdaryo", "Samarqand",
    "Qashqadaryo", "Surxondaryo", "Xorazm", "Qoraqalpog'iston Resp."
]

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

class Form(StatesGroup):
    name = State()
    surname = State()
    age = State()
    region = State()
    phone = State()
    check_sub = State()
    quiz = State()

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Xotira uchun o'zgaruvchilar
finished_users = set()
finished_names = set()
timer_tasks = {} # Taymerlarni saqlash uchun lug'at

# ==========================================
# HANDLERLAR
# ==========================================

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id in finished_users:
        await message.answer("Siz testni topshirib bo'lgansiz. Qayta ishtirok eta olmaysiz.")
        return
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Tanlovda ishtirok etish")]], resize_keyboard=True)
    await message.answer(f"Salom {message.from_user.first_name}! O'zbekiston Bolalar Tashkiloti tanlov botiga xush kelibsiz.", reply_markup=kb)

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
        await message.answer("Iltimos, yoshingizni faqat son bilan kiriting:")
        return
    
    age = int(message.text)
    if age > 18:
        await message.answer("<b>Uzr!</b> Tanlovda faqat 18 yosh va undan kichiklar qatnashishi mumkin.", parse_mode="HTML")
        await state.clear()
        return

    await state.update_data(age=age)
    
    kb_list = [REGIONS[i:i + 2] for i in range(0, len(REGIONS), 2)]
    region_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=col) for col in row] for row in kb_list],
        resize_keyboard=True
    )
    
    await message.answer("Yashash viloyatingizni tanlang:", reply_markup=region_kb)
    await state.set_state(Form.region)

@dp.message(Form.region)
async def process_region(message: types.Message, state: FSMContext):
    if message.text not in REGIONS:
        await message.answer("Iltimos, pastdagi tugmalardan birini tanlang!")
        return
        
    await state.update_data(region=message.text)
    phone_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]], resize_keyboard=True)
    await message.answer("Rahmat! Endi telefon raqamingizni yuboring (yoki kiriting):", reply_markup=phone_kb)
    await state.set_state(Form.phone)

@dp.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    # Agar foydalanuvchi kontakt yuborgan bo'lsa uni olamiz, bo'lmasa matnni olamiz
    phone_number = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone_number)
    
    check_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="✅ Obunani tekshirish")]], resize_keyboard=True)
    
    text = (
        "<b>Ishtirok etish uchun quyidagi sahifalarimizga obuna bo'ling:</b>\n\n"
        "1. Instagram: https://www.instagram.com/bolalartashkiloti/\n"
        "2. Telegram: https://t.me/bolalartashkilotiuz\n"
        "3. Telegram: https://t.me/xasanboy_nabiyev\n\n"
        "<i>Eslatma: Iltimos, barcha kanallarga obuna bo'ling va pastdagi tugmani bosing!</i>"
    )
    await message.answer(text, reply_markup=check_kb, disable_web_page_preview=True)
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
        await message.answer("Rahmat! Obuna tasdiqlandi. Testni boshlashingiz mumkin.", reply_markup=go_quiz_kb)
    else:
        text = "Siz hali Telegram kanallarimizga obuna bo'lmadingiz:\n" + "\n".join(not_subbed)
        await message.answer(text)

@dp.message(F.text == "🚀 Testni boshlash")
async def start_quiz_logic(message: types.Message, state: FSMContext):
    # Testni boshlash vaqtini xotiraga yozish
    await state.update_data(score=0, current_q=0, start_time=datetime.now().timestamp())
    await send_quiz_question(message.chat.id, message.from_user.id, state)

# ==========================================
# SAVOL YUBORISH VA TAYMER MANTIQI
# ==========================================
async def send_quiz_question(chat_id: int, user_id: int, state: FSMContext):
    data = await state.get_data()
    q_idx = data.get('current_q', 0)
    
    # Agar barcha savollar tugasa natijani chiqarish
    if q_idx >= len(QUIZ_DATA):
        await finish_quiz_logic(chat_id, user_id, state)
        return
        
    question = QUIZ_DATA[q_idx]
    opts = [[KeyboardButton(text=opt)] for opt in question['o']]
    kb = ReplyKeyboardMarkup(keyboard=opts, resize_keyboard=True)
    
    msg_text = f"<b>Savol {q_idx+1}:</b>\n\n{question['q']}\n\n⏱ <i>Ushbu savol uchun sizga 15 soniya vaqt berildi!</i>"
    await bot.send_message(chat_id, msg_text, reply_markup=kb)
    await state.set_state(Form.quiz)

    # Avvalgi taymerni to'xtatish (agar mavjud bo'lsa)
    if user_id in timer_tasks:
        timer_tasks[user_id].cancel()
        
    # Yangi 15 soniyalik taymerni yoqish
    timer_tasks[user_id] = asyncio.create_task(question_timeout(chat_id, user_id, state, q_idx))

async def question_timeout(chat_id: int, user_id: int, state: FSMContext, q_idx: int):
    try:
        await asyncio.sleep(15) # 15 soniya kutamiz
        data = await state.get_data()
        
        # Agar 15 soniyadan keyin ham foydalanuvchi ayni shu savolda bo'lsa, vaqt tugadi!
        if data.get('current_q', 0) == q_idx:
            await bot.send_message(chat_id, "⏳ <b>Vaqt tugadi!</b> Siz ushbu savolga javob berishga ulgurmadingiz.")
            await state.update_data(current_q=q_idx + 1)
            await send_quiz_question(chat_id, user_id, state) # Keyingi savolga o'tkazish
    except asyncio.CancelledError:
        # Foydalanuvchi vaqtida javob borgan bo'lsa, taymer to'xtatiladi (Cancel qilinadi)
        pass

@dp.message(Form.quiz)
async def handle_quiz_answer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    q_idx = data.get('current_q', 0)
    score = data.get('score', 0)
    
    valid_answers = QUIZ_DATA[q_idx]['o']
    if message.text not in valid_answers:
        await message.answer("Iltimos, pastdagi tugmalardan birini tanlang!")
        return

    # To'g'ri vaqtda javob berildi, taymerni to'xtatamiz
    if user_id in timer_tasks:
        timer_tasks[user_id].cancel()

    # Javobni tekshirish
    if message.text == QUIZ_DATA[q_idx]['a']:
        score += 1
        
    await state.update_data(score=score, current_q=q_idx + 1)
    await send_quiz_question(message.chat.id, user_id, state)

# ==========================================
# NATIJALAR (ADMIN VA FOYDALANUVCHIGA)
# ==========================================
async def finish_quiz_logic(chat_id: int, user_id: int, state: FSMContext):
    data = await state.get_data()
    
    # Qayta ishlamasligi uchun ro'yxatga qo'shamiz
    finished_users.add(user_id)
    name = data.get("name", "").strip().title()
    surname = data.get("surname", "").strip().title()
    finished_names.add(f"{name}|{surname}")

    score = data.get('score', 0)
    start_time = data.get('start_time')
    time_taken = datetime.now().timestamp() - start_time
    
    # Vaqtni formatlash (Daqiqa va soniya)
    mins = int(time_taken // 60)
    secs = int(time_taken % 60)
    time_str = f"{mins} daqiqa {secs} soniya" if mins > 0 else f"{secs} soniya"

    # Foydalanuvchiga boradigan xabar
    user_msg = (
        f"🎉 <b>Tabriklaymiz! Test yakunlandi.</b>\n\n"
        f"✅ Natijangiz: {len(QUIZ_DATA)} ta savoldan <b>{score} tasiga to'g'ri</b> javob berdingiz.\n"
        f"⏱ Testni ishlash uchun sarflagan vaqtingiz: <b>{time_str}</b>."
    )
    await bot.send_message(chat_id, user_msg, reply_markup=ReplyKeyboardRemove())
    
    # Adminga boradigan xabar
    admin_msg = (
        f"🔔 <b>YANGI NATIJA KELDI:</b>\n\n"
        f"👤 <b>F.I.SH:</b> {name} {surname}\n"
        f"📅 <b>Yoshi:</b> {data.get('age', 'Noma\\'lum')}\n"
        f"📍 <b>Viloyat:</b> {data.get('region', 'Noma\\'lum')}\n"
        f"📞 <b>Raqam:</b> {data.get('phone', 'Kiritilmagan')}\n"
        f"📊 <b>Ball:</b> {score} / 15\n"
        f"⏱ <b>Umumiy sarflangan vaqt:</b> {time_str}"
    )
    
    try:
        await bot.send_message(ADMIN_ID, admin_msg)
    except Exception as e:
        logging.error(f"Adminga xabar yuborishda xato: {e}")
        
    await state.clear()

# ==========================================
# WEB SERVER & ASYNCIO MAIN
# ==========================================
async def handle_ping(request):
    return web.Response(text="Bot muvaffaqiyatli ishlamoqda!")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Botni ishga tushirish
    asyncio.create_task(dp.start_polling(bot))

    # Web-serverni ishga tushirish (Render va boshqalar uchun)
    app = web.Application()
    app.router.add_get('/', handle_ping)
    
    port = int(os.environ.get("PORT", 10000)) 
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"Server {port}-portda ishga tushdi va bot polling qilmoqda...")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
