from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# === Replace with your token ===
import os
TOKEN = os.environ.get("8045556316:AAGYBBYFHU71Vsz56qdda8H0-RYPmRfanwE")


# Path to folder containing PDFs
PDF_PATH = r"C:\Users\pc\Downloads\bot\pdfs"

# Category -> Novel -> File mapping
NOVELS = {
    "Japanese": {
        "The Empty Box and Zeroth Maria": "The Empty Box and Zeroth Maria - Volume 01 [Yen Press][Kobo_LNWNCentral].pdf",
        "NieR Automata": "NieR Automata - Volume 01 - Long Story Short [VIZ][Kindle_LNWNCentral].pdf"
    },
    "Chinese": {
        "Heavenly Sword": "heavenly_sword.pdf",
        "Another CN": "another_cn.pdf"
    },
    "Korean": {
        "Omniscient Reader's Viewpoint (ORV)": "Omniscient Reader's Viewpoint.pdf",
        "Solo Leveling": "solo_leveling.pdf"
    }
}

# === Start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat|{cat}")] for cat in NOVELS.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 Choose a category:", reply_markup=reply_markup)

# === Handle category selection ===
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, category = query.data.split("|")

    novels = NOVELS.get(category, {})
    keyboard = [[InlineKeyboardButton(novel, callback_data=f"novel|{category}|{novel}")]
                for novel in novels.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=f"📖 Choose a novel from *{category}*:", 
                                  reply_markup=reply_markup, parse_mode="Markdown")

# === Handle novel selection (send PDF) ===
async def novel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, category, novel = query.data.split("|")

    filename = NOVELS[category][novel]
    file_path = os.path.join(PDF_PATH, filename)

    if os.path.exists(file_path):
        await query.message.reply_document(open(file_path, "rb"), filename=filename)
    else:
        await query.message.reply_text(f"⚠️ File not found: {filename}")

# === Main ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_handler, pattern="^cat\\|"))
    app.add_handler(CallbackQueryHandler(novel_handler, pattern="^novel\\|"))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


