# ТелеБот
import telebot
from telebot import types
from football_elo.player import PlayersDatabase
from football_elo.match import Match

# Сюда подставляете свой токен
bot = telebot.TeleBot('2105483477:AAEd8p7QxIqaUbXci4LEu3WxGJ_u1Lz8dgY')
player_database = PlayersDatabase(path=r"PlayersList.csv") #path=r"C:\Users\Shinobu\PlayersList.csv"
current_players = set()
current_match = Match()
current_teams = None

# Из примера с гитхаба, для умения считывать текст набранный ручками
# https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/custom_states.py


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('⚽️ Матч')
    markup.add(but1)
    bot.send_message(message.chat.id, 'Будем начинать'.format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['raiting'])
def raiting(message):
    bot.send_message(message.chat.id, player_database.show_rating())


@bot.message_handler(commands=['edit'])
def edit(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('🛠️ Добавить/Изменить')
    markup.add(but1)
    bot.send_message(message.chat.id, 'будем поменять'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    global current_match
    global current_teams

    if message.text == '⚽️ Матч':
        current_players.clear()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('1. Выбор игроков')
        but2 = types.KeyboardButton('2. Количество команд')
        but3 = types.KeyboardButton('3. Получить команды')
        but4 = types.KeyboardButton('4. Итог матча')
        markup.add(but1, but2, but3, but4)
        bot.send_message(message.chat.id, '⚽️ Матч', reply_markup=markup)

    elif message.text == '1. Выбор игроков':
        list_of_names = player_database.players.name.tolist()
        keyboard = types.InlineKeyboardMarkup(row_width=3)  # row_width - количество столбцов !!!!
        backbutton = types.InlineKeyboardButton(text='Готово', callback_data='1_Готово')
        button_list = [types.InlineKeyboardButton(text=x, callback_data=f'1_{x}')
                       for x in list_of_names]
        keyboard.add(*button_list, backbutton)
        bot.send_message(message.chat.id, '1. Выбор игроков', reply_markup=keyboard)
        # Блок сделал, вроде работает, но проблема с добавлением игроков в обнофлении вызвываемой функции.


    elif message.text == '2. Количество команд':
        l = ['2 команды', '3 команды', '4 команды']
        keyboard = types.InlineKeyboardMarkup(row_width=3)  # row_width - количество столбцов !!!!
        button_list = [types.InlineKeyboardButton(text=x, callback_data=x) for x in l]
        keyboard.add(*button_list)
        bot.send_message(message.chat.id, '2. Количество команд', reply_markup=keyboard)
        # Блок сделал, вроде работает


    elif message.text == '3. Получить команды':
        current_match = Match.load_from_player_list(current_players, player_database)
        current_teams = current_match.balance_teams()

        team_a = [player['name'] for player in current_teams[0]]
        team_b = [player['name'] for player in current_teams[1]]

        bot.send_message(message.chat.id, text=", ".join(team_a))
        bot.send_message(message.chat.id, text=", ".join(team_b))
        # Блок сделал, хз пока ошибка


    elif message.text == '4. Итог матча':
        l4 = []
        team_a = [player['name'] for player in current_teams[0]]
        team_b = [player['name'] for player in current_teams[1]]

        # Кнопки итога матча
        t1 = team_a[0]
        t2 = team_b[0]
        l4.append(t1)
        l4.append(t2)
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # row_width - количество столбцов !!!!
        backbutton = types.InlineKeyboardButton(text='Ничья', callback_data='4_Ничья')
        button_list = [types.InlineKeyboardButton(text=x, callback_data=f'4_{x}')
                       for x in l4]
        keyboard.add(*button_list)
        keyboard.add(backbutton)
        bot.send_message(message.chat.id, '4. Итог матча', reply_markup=keyboard)
        # Блок сделал, не проверял

    elif message.text == '🛠️ Добавить/Изменить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('6. Добавить человечка')
        but2 = types.KeyboardButton('7. Удалить человечка')
        markup.add(but1, but2)
        bot.send_message(message.chat.id, '🛠️ Добавить/Изменить', reply_markup=markup)


    elif message.text == '6. Добавить человечка':
        bot.send_message(message.chat.id,
                         'Сюда вписать имя добровольца. Начинаться имя должно с "New__" (пример New_Петя)')

        # здесь вроде запоминает введенное имя


    elif message.text == '7. Удалить человечка':
        list_of_names = player_database.players.name.tolist()
        keyboard = types.InlineKeyboardMarkup(row_width=3)  # row_width - количество столбцов !!!!
        button_list = [types.InlineKeyboardButton(text=x, callback_data=f'7_{x}') for x in list_of_names]
        keyboard.add(*button_list)
        bot.send_message(message.chat.id, 'Здесь выбирается из списка человечек и вылетает из нашей базы',
                         reply_markup=keyboard)



    elif message.text.startswith('New_'):
        player_database.add_player(name=message.text[4:])
        for x in player_database.players.name.tolist():
            bot.send_message(message.chat.id, x)


@bot.callback_query_handler(func=lambda call: call.data.startswith('1_'))
def handle1(call):  # 1. Выбор игроков
    player = call.data[2:]
    #    ls = []
    if player in player_database.names_list():
        current_players.add(player)
        bot.send_message(call.message.chat.id, player)

    if call.data == '1_Готово':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="1. Выбор игроков", reply_markup=None)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Выбор игроков закончен")


@bot.callback_query_handler(func=lambda call: call.data.startswith('4_'))
def handle4(call):  # 4. Итог матча
    win = None
    global current_teams
    global current_match
    global current_players
    team_a = set([player['name'] for player in current_teams[0]])
    team_b = set([player['name'] for player in current_teams[1]])
    player_name = call.data[2:]
    if player_name in team_a:
        win = 1
        bot.send_message(call.message.chat.id, 'Победила команда 1')
        current_match.set_result("win")
    elif player_name in team_b:
        win = 2
        bot.send_message(call.message.chat.id, 'Победила команда 2')
        current_match.set_result("lose")
    elif call.data == '4_Ничья':
        win = 0
        bot.send_message(call.message.chat.id, 'Ничья')
        current_match.set_result("draw")
    current_match.update_database(player_database)
    current_teams = None
    current_match = Match()
    current_players.clear()


@bot.callback_query_handler(func=lambda call: call.data.startswith('7_'))
def handle4(call):  # 7. Удалить человечка
    player_name = call.data[2:]
    player_database.players = player_database.remove_player(remove_name=player_name)
    bot.send_message(call.message.chat.id, 'Проверяем, удалился ли человечек')
    for x in player_database.players.name.tolist():
        bot.send_message(call.message.chat.id, x)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == '2 команды':
        bot.send_message(call.message.chat.id, '2 команды, классика')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="2. Количество команд", reply_markup=None)
    elif call.data == '3 команды':
        bot.send_message(call.message.chat.id, '3 команды, по 7 минут, делимся сами и записываем результат')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="2. Количество команд", reply_markup=None)
    elif call.data == '4 команды':
        bot.send_message(call.message.chat.id, '4 команды, ага, почти поверил.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="2. Количество команд", reply_markup=None)


bot.polling(non_stop=True)
