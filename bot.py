import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Инициализируем бота с твоим токеном
bot = telebot.TeleBot("8158112355:AAHUsjDUyExW0-nAM-OjANUd3u6mm-_NXwY")

# Словарь для хранения состояния пользователей
user_state = {}
# Словарь для отслеживания допрошенных персонажей
user_interrogations = {}
# Словарь для отслеживания, получил ли пользователь жетон
user_tokens = {}

# Экран 1: Вступление
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_state[user_id] = 'start'
    user_interrogations[user_id] = []  # Инициализируем список допрошенных
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🎩 Расследовать тайну"))
    
    bot.send_message(
        message.chat.id,
        "🕯️ *Добро пожаловать в Villa Sera* — казино, укрытое в тенях альпийских скал. 🎶\n"
        "Здесь играют не на деньги, а на *честь*, *стиль*… и *тайны*.\n\n"
        "Сегодня — закрытый вечер, только для избранных. Но что-то пошло не так…\n"
        "Главная фишка, дающая право на *коктейль вне меню*, исчезла.\n"
        "Бармен Лука склоняется к тебе, его голос — шёпот над бокалом:\n"
        "_“Раскрой, кто её забрал, и она станет твоей…”_ 🍸",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# Обработчик текстовых сообщений и кнопок
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Экран 1: Переход к осмотру
    if user_state.get(user_id) == 'start' and text == "🎩 Расследовать тайну":
        user_state[user_id] = 'inspection'
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("🥂 Мадам Эльза"))
        markup.add(KeyboardButton("🎷 Джанни, музыкант"))
        markup.add(KeyboardButton("🎲 Бруно, крупье"))
        
        bot.send_message(
            message.chat.id,
            "🕯️ Ты оглядываешь зал: мерцание свечей, мягкий джаз, шорох карт на столах. 🎶\n"
            "Всё замерло, будто время остановилось. Но в полумраке ты замечаешь *трёх гостей*, чьи тени хранят секреты.\n"
            "_Кого допросить первым?_",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    # Экран 2: Диалоги
    elif user_state.get(user_id) == 'inspection':
        if text in ["🥂 Мадам Эльза", "🎷 Джанни, музыкант", "🎲 Бруно, крупье"]:
            if text not in user_interrogations.get(user_id, []):
                user_interrogations[user_id].append(text)
            
            # Показываем диалог в зависимости от выбранного персонажа
            if text == "🥂 Мадам Эльза":
                bot.send_message(
                    message.chat.id,
                    "🥂 *Мадам Эльза* поправляет жемчужное ожерелье и улыбается:\n"
                    "_“Я приехала из Милана ради этого вечера… Как быстро ты раскроешь мою игру?”_",
                    parse_mode='Markdown'
                )
            
            elif text == "🎷 Джанни, музыкант":
                bot.send_message(
                    message.chat.id,
                    "🎷 *Джанни* отрывается от саксофона, его глаза блестят:\n"
                    "_“Я лишь играю мелодии. Но иногда слышу больше, чем вижу…”_",
                    parse_mode='Markdown'
                )
            
            elif text == "🎲 Бруно, крупье":
                bot.send_message(
                    message.chat.id,
                    "🎲 *Бруно* поправляет манжеты, его голос холоден:\n"
                    "_“Я видел всех. Кроме одного, кто за весь вечер ни разу не коснулся бокала.”_",
                    parse_mode='Markdown'
                )
            
            # Проверяем, допрошены ли все персонажи
            if len(user_interrogations.get(user_id, [])) == 3:
                user_state[user_id] = 'suspect_choice'
                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add(KeyboardButton("🕵️ Эльза"))
                markup.add(KeyboardButton("🎷 Джанни"))
                markup.add(KeyboardButton("🎲 Бруно"))
                
                bot.send_message(
                    message.chat.id,
                    "🕯️ Ты выслушал всех. Их слова эхом отдаются в твоей голове.\n"
                    "*Кто, по-твоему, ведёт себя подозрительнее всех?*",
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
            else:
                # Показываем кнопки только для недопрошенных персонажей
                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                if "🥂 Мадам Эльза" not in user_interrogations[user_id]:
                    markup.add(KeyboardButton("🥂 Мадам Эльза"))
                if "🎷 Джанни, музыкант" not in user_interrogations[user_id]:
                    markup.add(KeyboardButton("🎷 Джанни, музыкант"))
                if "🎲 Бруно, крупье" not in user_interrogations[user_id]:
                    markup.add(KeyboardButton("🎲 Бруно, крупье"))
                
                bot.send_message(
                    message.chat.id,
                    "🕯️ *Кого допросить дальше?*",
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
        
        else:
            bot.send_message(
                message.chat.id,
                "🕯️ *Выбери гостя*, нажав на кнопку. В этом зале случайностей не бывает.",
                parse_mode='Markdown'
            )
    
    # Экран 3: Выбор подозреваемого
    elif user_state.get(user_id) == 'suspect_choice':
        if text == "🕵️ Эльза":
            user_state[user_id] = 'evidence'
            
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton("🕯️ Перейти к загадке"))
            
            bot.send_message(
                message.chat.id,
                "🍸 Лука неспешно протирает бокал и кладёт перед тобой *три предмета*:\n"
                "— 🧿 *Брошь* с гравировкой *V.S.* (Villa Sera), найденная у стойки.\n"
                "— 📜 *Пачка нот* с вырванной страницей.\n"
                "— 🃏 *Игральная карта* с пятном аперитива.\n\n"
                "_“Следы — это маски. Но ты уже близко…”_",
                reply_markup=markup,
                parse_mode='Markdown'
            )
        
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton("🕵️ Эльза"))
            markup.add(KeyboardButton("🎷 Джанни"))
            markup.add(KeyboardButton("🎲 Бруно"))
            
            bot.send_message(
                message.chat.id,
                "❌ Лука усмехается, тень свечи дрожит на его лице:\n"
                "_“Почти, но не то. Взгляни внимательнее…”_",
                reply_markup=markup,
                parse_mode='Markdown'
            )
    
    # Экран 4: Переход к загадке
    elif user_state.get(user_id) == 'evidence' and text == "🕯️ Перейти к загадке":
        user_state[user_id] = 'riddle'
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("🥂 Эльза"))
        markup.add(KeyboardButton("🎷 Джанни"))
        markup.add(KeyboardButton("🎲 Бруно"))
        
        bot.send_message(
            message.chat.id,
            "🕯️ Лука подаёт тебе *салфетку*, исписанную мелким почерком:\n\n"
            "_Она пришла позже всех, но знала, где спрятан приз._\n"
            "_Он не уходил со сцены, но не видел, кто входил._\n"
            "_А тот, кто весь вечер не делал глотка — просто не хотел быть пойманным._\n\n"
            "**Кто взял фишку?**",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    # Экран 5: Загадка
    elif user_state.get(user_id) == 'riddle':
        if text == "🥂 Эльза":
            user_state[user_id] = 'final'
            
            bot.send_message(
                message.chat.id,
                "💡 *Ты разгадал тайну.* Это была **Эльза**. Но не ради выгоды…\n"
                "Она проверяла тебя. Или, может, прикрывала кого-то ещё?\n\n"
                "Лука кивает, его глаза блестят в полумраке:\n"
                "_“Ты один из нас. Villa Sera открывает свои тайны только избранным.”_\n\n"
                "🗝️ Назови слово *“СИЦИЛИЯ”*, чтобы получить жетон.\n"
                "_Каждому — лишь раз. Но у каждой тайны есть продолжение…_",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode='Markdown'
            )
        
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton("🥂 Эльза"))
            markup.add(KeyboardButton("🎷 Джанни"))
            markup.add(KeyboardButton("🎲 Бруно"))
            
            bot.send_message(
                message.chat.id,
                "❌ Лука качает головой, тень свечи скользит по стойке:\n"
                "_“Не совсем. Прочитай салфетку ещё раз…”_",
                reply_markup=markup,
                parse_mode='Markdown'
            )
    
    # Экран 6: Финал и проверка кодового слова
    elif user_state.get(user_id) == 'final':
        if text.lower() == "сицилия" and user_id not in user_tokens:
            user_tokens[user_id] = True
            bot.send_message(
                message.chat.id,
                "🗝️ *Лука улыбается, пряча взгляд за бокалом:*\n"
                "_“Добро пожаловать в круг избранных. Твой жетон у тебя.”_\n"
                "История *Villa Sera* только начинается… 🎶",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode='Markdown'
            )
        elif text.lower() == "сицилия" and user_id in user_tokens:
            bot.send_message(
                message.chat.id,
                "🍸 *Лука смеётся, разливая аперитив:*\n"
                "_“Ты уже получил свой жетон. Не жадничай, друг.”_",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                message.chat.id,
                "🕯️ *Лука хмурится, его голос становится тише:*\n"
                "_“Назови правильное слово. Без него жетона не видать.”_",
                parse_mode='Markdown'
            )

# Запускаем бота
bot.polling()