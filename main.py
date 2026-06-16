import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", "")
CLINIC_CHAT_ID = int(os.environ.get("CLINIC_CHAT_ID", "341149071"))
ADMIN_ID = int(os.environ.get("CLINIC_CHAT_ID", "341149071"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

(CHOOSE_POSITION, NAME, AGE, LOCATION, PHONE, EDUCATION, COURSES,
 CLINIC_NAME, DURATION, SPECIALTY, IMPLANT_BRANDS, DUTIES, REASON,
 SOFTWARE, STERILIZATION, OTHER_SKILLS, EXPERIENCE, WHY_MOAZZEN,
 SALARY, FULLTIME, ABOUT_ME, PRIVATE_MSG, CONFIRM) = range(23)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🦷 دندانپزشک", callback_data="pos_dentist"),
         InlineKeyboardButton("👩‍⚕️ دستیار تخصصی", callback_data="pos_assistant")],
        [InlineKeyboardButton("🗂️ منشی حرفه‌ای", callback_data="pos_secretary"),
         InlineKeyboardButton("👔 سوپروایزر", callback_data="pos_supervisor")],
        [InlineKeyboardButton("✉️ پیام خصوصی به مدیر", callback_data="pos_private")]
    ]
    return InlineKeyboardMarkup(keyboard)

def nav_keyboard():
    keyboard = [["🔄 شروع از ابتدا", "⬅️ بازگشت"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def confirm_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ ارسال رزومه", callback_data="confirm_yes")],
        [InlineKeyboardButton("✏️ ویرایش مجدد", callback_data="confirm_no")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    welcome_text = (
        "🦷 *کلینیک دندانپزشکی مؤذن*\n\n"
        "سلام و خوش آمدید 😊\n"
        "ممنون از علاقه‌ات به همکاری با ما!\n\n"
        "لطفاً موقعیت شغلی مورد نظرت رو انتخاب کن:"
    )
    msg = update.message if update.message else update.callback_query.message
    try:
        with open("/app/welcome.jpg", "rb") as photo:
            await msg.reply_photo(photo=photo, caption=welcome_text, parse_mode="Markdown", reply_markup=main_menu())
    except:
        await msg.reply_text(welcome_text, parse_mode="Markdown", reply_markup=main_menu())
    return CHOOSE_POSITION

async def choose_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    positions = {
        "pos_dentist": "دندانپزشک",
        "pos_assistant": "دستیار تخصصی",
        "pos_secretary": "منشی حرفه‌ای",
        "pos_supervisor": "سوپروایزر",
    }
    if query.data == "pos_private":
        await query.message.reply_text("✉️ پیامت رو بنویس، مستقیم به مدیر میرسه 📩", reply_markup=nav_keyboard())
        return PRIVATE_MSG
    if query.data in positions:
        context.user_data['position'] = positions[query.data]
        await query.message.reply_text(f"✅ انتخاب کردی: *{positions[query.data]}*\n\nنام و نام خانوادگی:", parse_mode="Markdown", reply_markup=nav_keyboard())
        return NAME
    return CHOOSE_POSITION

async def private_msg(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text: return await start(update, context)
    sender = update.effective_user
    await context.bot.send_message(chat_id=CLINIC_CHAT_ID, text=f"✉️ پیام خصوصی از @{sender.username or sender.first_name}:\n\n{text}")
    await update.message.reply_text("✅ پیامت به مدیر رسید!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def get_name(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("پوزیشن رو انتخاب کن:", reply_markup=main_menu())
        return CHOOSE_POSITION
    context.user_data['name'] = text
    await update.message.reply_text("سن:", reply_markup=nav_keyboard())
    return AGE

async def get_age(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("نام و نام خانوادگی:", reply_markup=nav_keyboard())
        return NAME
    context.user_data['age'] = text
    await update.message.reply_text("محل سکونت:", reply_markup=nav_keyboard())
    return LOCATION

async def get_location(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("سن:", reply_markup=nav_keyboard())
        return AGE
    context.user_data['location'] = text
    await update.message.reply_text("شماره تماس:", reply_markup=nav_keyboard())
    return PHONE

async def get_phone(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("محل سکونت:", reply_markup=nav_keyboard())
        return LOCATION
    context.user_data['phone'] = text
    await update.message.reply_text("رشته تحصیلی:", reply_markup=nav_keyboard())
    return EDUCATION

async def get_education(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("شماره تماس:", reply_markup=nav_keyboard())
        return PHONE
    context.user_data['education'] = text
    position = context.user_data.get('position', '')
    if position == "دندانپزشک":
        await update.message.reply_text("شماره نظام پزشکی:", reply_markup=nav_keyboard())
    else:
        await update.message.reply_text("دوره‌های تخصصی گذرونده (اگه نداری بنویس ندارم):", reply_markup=nav_keyboard())
    return COURSES

async def get_courses(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("رشته تحصیلی:", reply_markup=nav_keyboard())
        return EDUCATION
    context.user_data['courses'] = text
    await update.message.reply_text("نام کلینیک / مطب:", reply_markup=nav_keyboard())
    return CLINIC_NAME

async def get_clinic_name(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("دوره‌های تخصصی:", reply_markup=nav_keyboard())
        return COURSES
    context.user_data['clinic_name'] = text
    await update.message.reply_text("مدت همکاری (از ... تا ...):", reply_markup=nav_keyboard())
    return DURATION

async def get_duration(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("نام کلینیک:", reply_markup=nav_keyboard())
        return CLINIC_NAME
    context.user_data['duration'] = text
    position = context.user_data.get('position', '')
    if position in ["دستیار تخصصی", "سوپروایزر", "دندانپزشک"]:
        await update.message.reply_text("تخصص / گرایش:", reply_markup=nav_keyboard())
        return SPECIALTY
    await update.message.reply_text("شرح وظایف:", reply_markup=nav_keyboard())
    return DUTIES

async def get_specialty(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("مدت همکاری:", reply_markup=nav_keyboard())
        return DURATION
    context.user_data['specialty'] = text
    if context.user_data.get('position') == "دستیار تخصصی" and "ایمپلنت" in text:
        await update.message.reply_text("با چه برندهای ایمپلنتی آشنا هستی؟", reply_markup=nav_keyboard())
        return IMPLANT_BRANDS
    context.user_data['implant_brands'] = "-"
    await update.message.reply_text("شرح وظایف:", reply_markup=nav_keyboard())
    return DUTIES

async def get_implant_brands(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("تخصص:", reply_markup=nav_keyboard())
        return SPECIALTY
    context.user_data['implant_brands'] = text
    await update.message.reply_text("شرح وظایف:", reply_markup=nav_keyboard())
    return DUTIES

async def get_duties(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("مدت همکاری:", reply_markup=nav_keyboard())
        return DURATION
    context.user_data['duties'] = text
    await update.message.reply_text("دلیل جدایی:", reply_markup=nav_keyboard())
    return REASON

async def get_reason(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("شرح وظایف:", reply_markup=nav_keyboard())
        return DUTIES
    context.user_data['reason'] = text
    await update.message.reply_text("آشنایی با نرم‌افزار مطب:", reply_markup=nav_keyboard())
    return SOFTWARE

async def get_software(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("دلیل جدایی:", reply_markup=nav_keyboard())
        return REASON
    context.user_data['software'] = text
    await update.message.reply_text("آشنایی با بیمه / استریلیزاسیون:", reply_markup=nav_keyboard())
    return STERILIZATION

async def get_sterilization(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("آشنایی با نرم‌افزار:", reply_markup=nav_keyboard())
        return SOFTWARE
    context.user_data['sterilization'] = text
    await update.message.reply_text("مهارت‌های دیگه:", reply_markup=nav_keyboard())
    return OTHER_SKILLS

async def get_other_skills(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("آشنایی با بیمه:", reply_markup=nav_keyboard())
        return STERILIZATION
    context.user_data['other_skills'] = text
    await update.message.reply_text("سال‌های سابقه در دندانپزشکی:", reply_markup=nav_keyboard())
    return EXPERIENCE

async def get_experience(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("مهارت‌های دیگه:", reply_markup=nav_keyboard())
        return OTHER_SKILLS
    context.user_data['experience'] = text
    await update.message.reply_text("چرا کلینیک مؤذن؟", reply_markup=nav_keyboard())
    return WHY_MOAZZEN

async def get_why(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("سال‌های سابقه:", reply_markup=nav_keyboard())
        return EXPERIENCE
    context.user_data['why'] = text
    await update.message.reply_text("حقوق مدنظر:", reply_markup=nav_keyboard())
    return SALARY

async def get_salary(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("چرا کلینیک مؤذن؟", reply_markup=nav_keyboard())
        return WHY_MOAZZEN
    context.user_data['salary'] = text
    await update.message.reply_text("امکان کار تمام‌وقت داری؟ (بله/خیر)", reply_markup=nav_keyboard())
    return FULLTIME

async def get_fulltime(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("حقوق مدنظر:", reply_markup=nav_keyboard())
        return SALARY
    context.user_data['fulltime'] = text
    await update.message.reply_text("درباره من ✍️\nهر چیزی که دوست داری درباره خودت بگی:", reply_markup=nav_keyboard())
    return ABOUT_ME

async def get_about_me(update, context):
    text = update.message.text
    if "شروع از ابتدا" in text: return await start(update, context)
    if "بازگشت" in text:
        await update.message.reply_text("امکان کار تمام‌وقت:", reply_markup=nav_keyboard())
        return FULLTIME
    context.user_data['about_me'] = text
    d = context.user_data
    summary = f"""📋 *خلاصه رزومه شما:*

👤 نام: {d.get('name', '-')}
🎂 سن: {d.get('age', '-')}
📍 محل سکونت: {d.get('location', '-')}
📞 تماس: {d.get('phone', '-')}
💼 موقعیت: {d.get('position', '-')}
🎓 تحصیلات: {d.get('education', '-')}
🏥 کلینیک قبلی: {d.get('clinic_name', '-')}
📅 مدت: {d.get('duration', '-')}
💰 حقوق: {d.get('salary', '-')}

آیا اطلاعات صحیح است و رزومه ارسال شود؟"""
    await update.message.reply_text(summary, parse_mode="Markdown", reply_markup=confirm_keyboard())
    return CONFIRM

async def confirm_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_no":
        await query.message.reply_text("از ابتدا شروع کن:", reply_markup=ReplyKeyboardRemove())
        return await start(update, context)
    d = context.user_data
    msg = f"""📋 رزومه جدید — {d.get('position', '')}

👤 اطلاعات شخصی:
نام: {d.get('name', '-')}
سن: {d.get('age', '-')}
محل سکونت: {d.get('location', '-')}
شماره تماس: {d.get('phone', '-')}

🎓 تحصیلات:
رشته: {d.get('education', '-')}
دوره‌ها/شماره نظام: {d.get('courses', '-')}

🏥 سابقه کاری:
نام کلینیک: {d.get('clinic_name', '-')}
مدت همکاری: {d.get('duration', '-')}
تخصص/سمت: {d.get('specialty', '-')}
برندهای ایمپلنت: {d.get('implant_brands', '-')}
شرح وظایف: {d.get('duties', '-')}
دلیل جدایی: {d.get('reason', '-')}

💡 مهارت‌ها:
نرم‌افزار: {d.get('software', '-')}
بیمه/استریلیزاسیون: {d.get('sterilization', '-')}
مهارت‌های دیگه: {d.get('other_skills', '-')}
سابقه دندانپزشکی: {d.get('experience', '-')}

❓ سوالات تکمیلی:
چرا مؤذن: {d.get('why', '-')}
حقوق مدنظر: {d.get('salary', '-')}
تمام‌وقت: {d.get('fulltime', '-')}

✍️ درباره من:
{d.get('about_me', '-')}"""
    await context.bot.send_message(chat_id=CLINIC_CHAT_ID, text=msg)
    await query.message.reply_text("✅ ممنون! رزومه‌ات ثبت شد و به زودی باهات تماس می‌گیریم 😊\n\n🦷 کلینیک دندانپزشکی مؤذن", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_POSITION: [CallbackQueryHandler(choose_position)],
            PRIVATE_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, private_msg)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_education)],
            COURSES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_courses)],
            CLINIC_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_clinic_name)],
            DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_duration)],
            SPECIALTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_specialty)],
            IMPLANT_BRANDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_implant_brands)],
            DUTIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_duties)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)],
            SOFTWARE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_software)],
            STERILIZATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sterilization)],
            OTHER_SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_other_skills)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            WHY_MOAZZEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_why)],
            SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_salary)],
            FULLTIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fulltime)],
            ABOUT_ME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_about_me)],
            CONFIRM: [CallbackQueryHandler(confirm_resume)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("Bot started...")
    if WEBHOOK_URL:
        app.run_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 8443)), url_path=TOKEN, webhook_url=f"{WEBHOOK_URL}/{TOKEN}")
    else:
        app.run_polling()

if __name__ == "__main__":
    main()
