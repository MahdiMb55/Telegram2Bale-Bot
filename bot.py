import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from worker import process_file

with open("config.json") as f:
    config = json.load(f)

is_processing = False

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_processing

    if is_processing:
        await update.message.reply_text("⛔ در حال پردازش فایل قبلی...")
        return

    user_id = str(update.message.from_user.id)

    if user_id not in config["user_map"]:
        await update.message.reply_text("⛔ دسترسی ندارید")
        return

    file = None
    if update.message.document:
        file = update.message.document
    elif update.message.video:
        file = update.message.video
    elif update.message.audio:
        file = update.message.audio

    if not file:
        await update.message.reply_text("❌ فایل نامعتبر")
        return

    is_processing = True

    await update.message.reply_text("⬇️ در حال دانلود...")

    try:
        await process_file(context.bot, file.file_id, file.file_name, user_id)
        await update.message.reply_text("✅ انجام شد")
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")
    finally:
        is_processing = False

app = ApplicationBuilder().token(config["telegram_bot_token"]).build()

app.add_handler(
    MessageHandler(
        filters.Document.ALL | filters.VIDEO | filters.AUDIO,
        handle_file
    )
)
app.run_polling()