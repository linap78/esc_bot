import flask
import telebot
from telebot import types
from datetime import date
import conf
import os
import random

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

eu_date = date(2022, 5, 10)
now = date.today()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="ESC 2022", callback_data="esc")
    button2 = types.InlineKeyboardButton(text="Случайный мем", callback_data="meme")
    button3 = types.InlineKeyboardButton(
        text="Слова песен: облако слов, квиз, основанный на работе с семантической моделью",
        callback_data="lyrics",
    )
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    bot.send_message(
        message.chat.id,
        "Привет! Это информационный бот о Евровидении: здесь ты можешь узнать последние новости о ESC2022, проверить, сколько дней осталось до первого полуфинала, попросить отправить случайный мем и посмотреть на всякие облака слов и баловство с семантической моделью, обученной на словах песен с Евровидений последних нескольких лет.",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "esc":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                text="Сколько дней до Евровидения?", callback_data="days"
            )
            button2 = types.InlineKeyboardButton(
                text="Где проводится?", callback_data="where"
            )
            button3 = types.InlineKeyboardButton(
                text="Купить билеты", callback_data="tickets"
            )
            button4 = types.InlineKeyboardButton(
                text="Последние новости на 31.03", callback_data="news"
            )
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)

            bot.send_message(
                call.message.chat.id,
                "Здесь можно узнать о Евровидении 2022: последние новости, сколько дней до первого полуфинала, где будет проводиться и как купить билеты",
                reply_markup=keyboard,
            )
        if call.data == "days":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="esc")
            keyboard.add(button1)

            bot.send_message(
                call.message.chat.id,
                "До Евровидения осталось {} дней".format((eu_date - now).days),
                reply_markup=keyboard,
            )
        if call.data == "where":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="esc")
            keyboard.add(button1)

            bot.send_message(
                call.message.chat.id,
                "Предстоящий 66-й конкурс песни «Евровидение» состоится в Турине (Италия), благодаря победе Måneskin с песней «Zitti e buoni» на конкурсе предыдущего года. Тури́н (итал. Torino [toˈriːno], пьем. Turin [tyˈɾiŋ])  — город в Италии, важный деловой и культурный центр северной Италии. Административный центр области Пьемонт и одноимённой территориальной единицы, приравненной к провинции. Четвёртый после Рима, Милана и Неаполя город Италии по количеству жителей, насчитывает около 876 тыс. чел. (2018), вместе с пригородами 1,7 миллиона человек.",
                reply_markup=keyboard,
            )
        if call.data == "tickets":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="esc")
            keyboard.add(button1)

            bot.send_message(
                call.message.chat.id,
                "Пока билеты не появились в продаже, но информацию об их появлении можно найти на официальном сайте: https://eurovision.tv/tickets-22",
                reply_markup=keyboard,
            )
        if call.data == "news":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                text="Давай!", callback_data="news_wordcloud"
            )
            button2 = types.InlineKeyboardButton(
                text="А что такое облако слов?", callback_data="whatis_wordcloud"
            )
            keyboard.add(button1)
            keyboard.add(button2)

            with open("eu_news.csv", "r", encoding="utf-8") as f:
                file = f.readlines()
                for line in file[1:]:
                    name, link, txt = line.strip().split("\t")
                    bot.send_message(call.message.chat.id, name + link)

            bot.send_message(
                call.message.chat.id,
                "Хочешь посмотреть на облако слов новостей на 27.03?",
                reply_markup=keyboard,
            )
        if call.data == "news_wordcloud":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="esc")
            keyboard.add(button1)

            photo = open("news_wordcloud.png", "rb")
            bot.send_photo(call.message.chat.id, photo)
            bot.send_message(call.message.chat.id, "Назад?", reply_markup=keyboard)
        if call.data == "whatis_wordcloud":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="esc")
            keyboard.add(button1)

            bot.send_message(
                call.message.chat.id,
                "Облако слов — один из видов визуализации текста. В зависимости от частотности слова меняется его размер на картинке.",
                reply_markup=keyboard,
            )

        if call.data == "meme":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Да", callback_data="meme")
            keyboard.add(button1)

            photos = [f for f in os.listdir() if ".jpg" in f]
            photo = open(random.choice(photos), "rb")
            bot.send_photo(call.message.chat.id, photo)
            bot.send_message(call.message.chat.id, "Ещё один?", reply_markup=keyboard)

        if call.data == "lyrics":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                text="Облако слов", callback_data="lyrics_wordcloud"
            )
            button2 = types.InlineKeyboardButton(
                text="Мини-квиз на основе семантической модели", callback_data="quiz"
            )
            button3 = types.InlineKeyboardButton(
                text="А что такое семантическая модель?", callback_data="whatis_model"
            )
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            bot.send_message(
                call.message.chat.id, "Выбери опцию", reply_markup=keyboard
            )
        if call.data == "lyrics_wordcloud":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="lyrics")
            keyboard.add(button1)

            photo = open("lyrics_wordcloud.png", "rb")
            bot.send_photo(call.message.chat.id, photo)
            bot.send_message(call.message.chat.id, "Назад?", reply_markup=keyboard)
        if call.data == "quiz":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Late", callback_data="r")
            button2 = types.InlineKeyboardButton(
                text="Libi (means beloved in Amharic)", callback_data="w"
            )
            button3 = types.InlineKeyboardButton(text="Need", callback_data="w")
            button4 = types.InlineKeyboardButton(text="Crime", callback_data="w")
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)

            bot.send_message(
                call.message.chat.id,
                "Какое слово, по версии модели, является ближайшим к love (все входят в топ-10 ближайших к love слов?",
                reply_markup=keyboard,
            )
        if call.data == "r":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="oh", callback_data="w2")
            button2 = types.InlineKeyboardButton(text="hey", callback_data="w2")
            button3 = types.InlineKeyboardButton(text="yay", callback_data="r2")
            button4 = types.InlineKeyboardButton(text="ah", callback_data="w2")
            button5 = types.InlineKeyboardButton(text="yeah", callback_data="w2")
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)
            keyboard.add(button5)

            bot.send_message(
                call.message.chat.id,
                "Верно! Какое слово, по версии модели, лишнее?",
                reply_markup=keyboard,
            )
        if call.data == "w":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="oh", callback_data="w2")
            button2 = types.InlineKeyboardButton(text="hey", callback_data="w2")
            button3 = types.InlineKeyboardButton(text="yay", callback_data="r2")
            button4 = types.InlineKeyboardButton(text="ah", callback_data="w2")
            button5 = types.InlineKeyboardButton(text="yeah", callback_data="w2")
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)
            keyboard.add(button5)

            bot.send_message(
                call.message.chat.id,
                "Нет, верный ответ — late! Какое слово, по версии модели, лишнее?",
                reply_markup=keyboard,
            )
        if call.data == "r2":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="hurray", callback_data="r3")
            button2 = types.InlineKeyboardButton(text="rainbow", callback_data="w3")
            button3 = types.InlineKeyboardButton(text="boogie", callback_data="w3")
            button4 = types.InlineKeyboardButton(text="confess", callback_data="w3")
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)

            photo = open("wisest_words.png", "rb")
            bot.send_photo(call.message.chat.id, photo)
            bot.send_message(
                call.message.chat.id,
                "Да! Вот визуализация векторов этих слов. А какое слово, по версии модели, ближе всего к yay?",
                reply_markup=keyboard,
            )
        if call.data == "w2":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="hurray", callback_data="r3")
            button2 = types.InlineKeyboardButton(text="rainbow", callback_data="w3")
            button3 = types.InlineKeyboardButton(text="boogie", callback_data="w3")
            button4 = types.InlineKeyboardButton(text="confess", callback_data="w3")
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)

            photo = open("wisest_words.png", "rb")
            bot.send_photo(call.message.chat.id, photo)
            bot.send_message(
                call.message.chat.id,
                "Нет, лишним было yay. Вот визуализация векторов этих слов. А какое слово, по версии модели, ближе всего к yay?",
                reply_markup=keyboard,
            )
        if call.data == "r3":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="lyrics")
            keyboard.add(button1)

            bot.send_message(call.message.chat.id, "Правильно!", reply_markup=keyboard)
        if call.data == "w3":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="lyrics")
            keyboard.add(button1)

            bot.send_message(
                call.message.chat.id, "Неправильно, это hurray", reply_markup=keyboard
            )

        if call.data == "whatis_model":

            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Назад", callback_data="lyrics")
            keyboard.add(button1)

            bot.send_message(
                call.message.chat.id,
                "Используемая в этом случае система Word2Vec — нейросеть, которая на основе корпуса (текстов песен с Евровидения) постепенно подбирает коэффициенты (значения в векторах) для каждого слова так, чтобы с помощью них можно было наилучшим образом предсказывать слова по контексту",
                reply_markup=keyboard,
            )


@app.route("/", methods=["GET", "HEAD"])
def index():
    return "ok"


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)
