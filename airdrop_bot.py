import logging
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Configuration - REPLACE THESE WITH YOUR ACTUAL LINKS
TOKEN = "7633421821:AAFSPBY1qvn1xRykILdQs5xSDi4D91Pi_0A"
CHANNEL_LINK = "https://t.me/your_channel"  # Replace with your channel link
GROUP_LINK = "https://t.me/your_group"      # Replace with your group link
TWITTER_LINK = "https://twitter.com/your_twitter"  # Replace with your Twitter link

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
TASKS, WALLET = range(2)

# Generate fake transaction ID
def generate_fake_tx_id(wallet):
    chars = "0123456789ABCDEF"
    prefix = ''.join(random.choices(chars, k=16))
    suffix = ''.join(random.choices(chars, k=16))
    return f"{prefix}...{suffix}{wallet[:4]}"

def start(update: Update, context: CallbackContext) -> int:
    """Send welcome message and tasks"""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ Done Tasks", callback_data='done_tasks')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Add typing effect for realism
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    time.sleep(1)
    
    update.message.reply_text(
        f"👋 Hello {user.mention_html()}!\n\n"
        "🎁 **GET FREE 10 SOL!** 🎁\n\n"
        "Complete these simple tasks to claim your reward:\n\n"
        "1. 📢 Join our official channel\n"
        "2. 👥 Join our community group\n"
        "3. 🐦 Follow us on Twitter\n\n"
        "Click ✅ **Done Tasks** when finished!",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    return TASKS

def button_handler(update: Update, context: CallbackContext) -> int:
    """Handle task completion button"""
    query = update.callback_query
    query.answer()
    
    if query.data == 'done_tasks':
        # Add processing effect
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        time.sleep(1)
        
        query.edit_message_text(
            "🎉 Awesome! Tasks completed!\n\n"
            "💰 Now send your Solana wallet address where we should send your 10 SOL:\n\n"
            "_(Example: 4Q3Wm... or just paste your wallet address)_"
        )
        return WALLET
    return TASKS

def handle_wallet(update: Update, context: CallbackContext) -> int:
    """Receive wallet address and show fake confirmation"""
    wallet = update.message.text.strip()
    
    # Generate fake transaction ID
    tx_id = generate_fake_tx_id(wallet)
    
    # Simulate processing
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    time.sleep(2)
    
    update.message.reply_text(
        f"✅ Wallet received: `{wallet[:12]}...{wallet[-4:]}`\n\n"
        "🚀 Processing transaction...",
        parse_mode="Markdown"
    )
    
    # Add artificial delay for "processing"
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    time.sleep(3)
    
    # Send fake success message
    update.message.reply_text(
        f"🎉 **CONGRATULATIONS!** 🎉\n\n"
        f"💸 **10 SOL** has been sent to your wallet!\n\n"
        f"🔹 Wallet: `{wallet[:12]}...{wallet[-4:]}`\n"
        f"🔹 Amount: 10 SOL\n"
        f"🔹 Transaction ID: `{tx_id}`\n"
        f"⏱ Estimated confirmation: 2 minutes\n\n"
        "✨ Thank you for participating in our airdrop!",
        parse_mode="Markdown"
    )
    
    # Add fake explorer link
    keyboard = [[InlineKeyboardButton("🔍 View on Solana Explorer", url="https://explorer.solana.com/")]]
    update.message.reply_text(
        "You can track your transaction on Solana Explorer:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """End conversation"""
    update.message.reply_text(
        '❌ Airdrop canceled. Type /start to begin again.',
        parse_mode="Markdown"
    )
    return ConversationHandler.END

def main() -> None:
    """Run bot"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TASKS: [CallbackQueryHandler(button_handler)],
            WALLET: [MessageHandler(Filters.text & ~Filters.command, handle_wallet)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    
    # Start the Bot
    updater.start_polling()
    logger.info("🚀 Airdrop bot is now running...")
    logger.info("⚙️ Note: This is a TEST bot - no real SOL is being sent")
    updater.idle()

if __name__ == '__main__':
    main()
