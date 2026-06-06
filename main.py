import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = os.environ.get("TOKEN", "")
CLINIC_CHAT_ID = int(os.environ.get("CLINIC_CHAT_ID", "341149071"))

CHOOSE_POSITION, NAME, AGE, LOCATION, PHONE, EDUCATION, COURSES, CLINIC_NAME, DURATION, SPECIALTY, IMPLANT_BRANDS, DUTIES, REASON, SOFTWARE, STERILIZATION, OTHER_SKILLS, EXPERIENCE, WHY_MOAZZEN, SALARY, FULLTIME = range(20)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["1️⃣ منشی حرفه‌ای"], ["2️⃣ دستیار تخصصی"], ["3️⃣ سوپروایزر"]]
    await update.message.reply_text(
        "سلام 😊\nممنون از علاقه‌ات به همکاری با کلینیک دندانپزشکی مؤذن!\n\nلطفاً پوزیشن مورد نظرت رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSE_POSITION

async def choose_position(update, context):
    text = update.message.text
    if "منشی" in text: context.user_data['position'] = "منشی حرفه‌ای"
    elif "دستیار" in text: context.user_data['position'] = "دستیار تخصصی"
    elif "سوپروایزر" in text: context.user_data['position'] = "سوپروایزر"
    else:
        await update.message.reply_text("لطفاً یکی از گزینه‌ها رو انتخاب کن.")
        return CHOOSE_POSITION
    await update.message.reply_text("نام و نام خانوادگی:", reply_markup=ReplyKeyboardRemove())
    return NAME

async def get_name(update, context):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("سن:")
    return AGE

async def get_age(update, context):
    context.user_data['age'] = update.message.text
    await update.message.reply_text("محل سکونت:")
    return LOCATION

async def get_location(update, context):
    context.user_data['location'] = update.message.text
    await update.message.reply_text("شماره تماس:")
    return PHONE

async def get_phone(update, context):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("رشته تحصیلی:")
    return EDUCATION

async def get_education(update, context):
    context.user_data['education'] = update.message.text
    await update.message.reply_text("دوره‌های تخصصی گذرونده (اگه نداری بنویس ندارم):")
    return COURSES

async def get_courses(update, context):
    context.user_data['courses'] = update.message.text
    await update.message.reply_text("نام کلینیک / مطب / پزشک:")
    return CLINIC_NAME

async def get_clinic_name(update, context):
    context.user_data['clinic_name'] = update.message.text
    await update.message.reply_text("مدت همکاری (از ... تا ...):")
    return DURATION

async def get_duration(update, context):
    context.user_data['duration'] = update.message.text
    position = context.user_data.get('position', '')
    if position in ["دستیار تخصصی", "سوپروایزر"]:
        await update.message.reply_text("چه تخصصی کار کردی / سمت:")
        return SPECIALTY
    await update.message.reply_text("شرح وظایف:")
    return DUTIES

async def get_specialty(update, context):
    context.user_data['specialty'] = update.message.text
    if context.user_data.get('position') == "دستیار تخصصی" and "ایمپلنت" in update.message.text.lower():
        await update.message.reply_text("با چه برندهای ایمپلنتی آشنا هستی؟")
        return IMPLANT_BRANDS
    context.user_data['implant_brands'] = "-"
    await update.message.reply_text("شرح وظایف:")
    return DUTIES

async def get_implant_brands(update, context):
    context.user_data['implant_brands'] = update.message.text
    await update.message.reply_text("شرح وظایف:")
    return DUTIES

async def get_duties(update, context):
    context.user_data['duties'] = update.message.text
    await update.message.reply_text("دلیل جدایی:")
    return REASON

async def get_reason(update, context):
    context.user_data['reason'] = update.message.text
    await update.message.reply_text("آشنایی با نرم‌افزار مطب / ابزار تخصصی:")
    return SOFTWARE

async def get_software(update, context):
    context.user_data['software'] = update.message.text
    await update.message.reply_text("آشنایی با بیمه تکمیلی / استریلیزاسیون:")
    return STERILIZATION

async def get_sterilization(update, context):
    context.user_data['sterilization'] = update.message.text
    await update.message.reply_text("مهارت‌های دیگه:")
    return OTHER_SKILLS

async def get_other_skills(update, context):
    context.user_data['other_skills'] = update.message.text
    await update.message.reply_text("سال‌های سابقه در دندانپزشکی:")
    return EXPERIENCE

async def get_experience(update, context):
    context.user_data['experience'] = update.message.text
    await update.message.reply_text("چرا کلینیک مؤذن؟")
    return WHY_MOAZZEN

async def get_why(update, context):
    context.user_data['why'] = update.message.text
    await update.message.reply_text("حقوق مدنظر:")
    return SALARY

async def get_salary(update, context):
    context.user_data['salary'] = update.message.text
    await update.message.reply_text("امکان کار تمام‌وقت داری؟ (بله/خیر)")
    return FULLTIME

async def get_fulltime(update, context):
    context.user_data['fulltime'] = update.message.text
    d = context.user_data
    msg = f"""📋 رزومه جدید — {d.get('position', '')}

👤 اطلاعات شخصی:
نام: {d.get('name', '-')}
سن: {d.get('age', '-')}
محل سکونت: {d.get('location', '-')}
شماره تماس: {d.get('phone', '-')}

🎓 تحصیلات:
رشته: {d.get('education', '-')}
دوره‌های تخصصی: {d.get('courses', '-')}

🏥 سابقه کاری:
نام کلینیک: {d.get('clinic_name', '-')}
مدت همکاری: {d.get('duration', '-')}
تخصص/سمت: {d.get('specialty', '-')}
برندهای ایمپلنت: {d.get('implant_brands', '-')}
شرح وظایف: {d.get('duties', '-')}
دلیل جدایی: {d.get('reason', '-')}

💡 مهارت‌ها:
{d.get('software', '-')}
{d.get('sterilization', '-')}
مهارت‌های دیگه: {d.get('other_skills', '-')}
سابقه دندانپزشکی: {d.get('experience', '-')}

❓ سوالات تکمیلی:
چرا مؤذن: {d.get('why', '-')}
حقوق مدنظر: {d.get('salary', '-')}
تمام‌وقت: {d.get('fulltime', '-')}"""

    await context.bot.send_message(chat_id=CLINIC_CHAT_ID, text=msg)
    await update.message.reply_text("✅ ممنون! رزومه‌ات ثبت شد و به زودی باهات تماس می‌گیریم 😊", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_position)],
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
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
