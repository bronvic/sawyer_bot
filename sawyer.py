import logging
import os
import signal
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import random
from scipy.stats import norm

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}: {signal.Signals(signum).name}")


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)


async def ahah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Handling ahah message")
    min_ah = 2
    max_ah = 11
    mu = 2
    sigma = 1.5

    distribution = norm(loc=mu, scale=sigma)

    syllables = round(distribution.rvs())
    syllables = max(min(syllables, max_ah), min_ah)

    response = "ах" * syllables

    if random.random() < 0.1:
        index = random.randint(1, len(response) - 2)
        response = response[:index] + response[index] + response[index:]

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Handling start command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="	🫠")


if __name__ == '__main__':
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    application = ApplicationBuilder().token(token).connect_timeout(15).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    ahah_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), ahah)
    application.add_handler(ahah_handler)

    lb_ip = os.environ.get('LB_IP')
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting webhook on {lb_ip}:{port}")
    application.run_webhook(webhook_url=lb_ip, listen="0.0.0.0", port=port)
