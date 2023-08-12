import os
from telegram import (
    ForceReply,
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from dotenv import load_dotenv
from helper import INIT, SUCCESS, handle_input

load_dotenv()
SECRET_KEY = os.environ.get("BOT_TOKEN")


reply_keyboard = [
    [{"text": "Yes", "callback_data": "y"}, {"text": "No", "callback_data": "n"}],
]

markup = InlineKeyboardMarkup(reply_keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    info = "What will you like to summarize today!"

    await update.message.reply_html(
        rf"Hi {user.mention_html()}! " + info,
        reply_markup=ForceReply(selective=True),
    )

    return INIT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Bye! Have a great day!.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the user message."""
    user_message = update.message.text
    state, response = handle_input(user_message)

    await update.message.reply_text(response)

    if state == SUCCESS:
        await update.message.reply_html(
            rf"Hi, would you like to make another summarization!",
            reply_markup=markup,
        )


async def decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    if update.callback_query.data == "y":
        return INIT
    else:
        await update.effective_message.edit_text("Bye! Have a great day!.")
        context.user_data.clear()
        return ConversationHandler.END


def main():
    application = Application.builder().token(SECRET_KEY).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    callback_handler = CallbackQueryHandler(decision)

    application.add_handler(conv_handler)
    application.add_handler(callback_handler)

    print("Bot initialized!")

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
