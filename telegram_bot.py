import os
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from llm_query import get_response

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the bot with your token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the /start command is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I'm your AI assistant. How can I help you today?",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when the /help command is issued."""
    await update.message.reply_text("You can ask me anything related to the documents I have access to.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and provide responses."""
    user_id = update.message.from_user.id
    user_message = update.message.text

    # Retrieve chat history for the user
    chat_history = context.user_data.get("chat_history", [])

    # Get response from the LLM
    response, updated_history = get_response(user_message, chat_history)

    # Save updated chat history
    context.user_data["chat_history"] = updated_history

    # Send the response back to the user
    await update.message.reply_text(response)

def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    print("Bot is running!")
    application.run_polling()

if __name__ == "__main__":
    main()