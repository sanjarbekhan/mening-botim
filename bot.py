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

if name == "main":
    asyncio.run(main())
