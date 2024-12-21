import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "7822766241:AAGjhwzu8Zl9ZGXoP88ru4hFBe0EM82VKZs" #os.getenv("BOT_TOKEN")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

 
game_state = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в угадай число!  Напиши /newgame чтобы начать.")

async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    secret_number = random.randint(1, 100)
    game_state[user_id] = {'secret': secret_number, 'guesses_left': 7}
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Я загадываю число между 1 и 100.  Какое число ты выбираешь?")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in game_state:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Начни новую игру написав /newgame")
        return

    try:
        guess = int(update.message.text)
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неправильный ввод. Пожалуйста, введите число.")
        return

    game = game_state[user_id]
    guesses_left = game['guesses_left'] -1
    secret = game['secret']
    if guess == secret:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Поздравляю! Вы угадали число {secret} за {7 - guesses_left} попыток!")
        del game_state[user_id]
    elif guess < secret:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Слишком маленькое! У вас осталось {guesses_left} попыток.")
        game['guesses_left'] = guesses_left
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Слишком большое! У вас осталось {guesses_left} попыток.")
        game['guesses_left'] = guesses_left
    if guesses_left == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"У вас закончились попытки! Загаданным числом было {secret}")
        del game_state[user_id]

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    newgame_handler = CommandHandler('newgame', newgame)
    guess_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, guess)

    application.add_handler(start_handler)
    application.add_handler(newgame_handler)
    application.add_handler(guess_handler)

    application.run_polling()


