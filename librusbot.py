import telebot
import schedule
from shudules import dif, queue_work
from message import librus_ads
import logging
import json

TOKEN = "token"
data_list = []
dict_secret = {}

# create and configuration to logging
# logging.basicConfig(filename="botLog.log", filemode="w",
#                     format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
#                     level=logging.INFO)

# Creates a new  bot's instance
bot = telebot.TeleBot(TOKEN)


# replicas for bot
with open("dialogs.json") as file:
    replicas = json.load(file)

# Function for processing command the "/start"
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, replicas["start"])


# Function for processing command the "/startlibrus"
@bot.message_handler(commands=["startlibrus"])
def startlibrus(message):
    strt_msg = bot.send_message(
        message.chat.id, replicas["Welcome"] + message.chat.first_name + replicas["startlibrus"])
    bot.register_next_step_handler(strt_msg, setup_librus)


# Function for reactions for connect/disconnect to Librus
def setup_librus(message):
    if message.text in ('да', 'yes', 'y', 'Y'):
        msg_login = bot.send_message(
            message.chat.id, replicas["Nice business"] + message.chat.first_name+replicas["librus login"])
        bot.register_next_step_handler(msg_login, librus_login)
    else:
        bot.send_message(message.chat.id,
                     replicas["librus cancel"] + message.chat.first_name)
        queue_work("no")


# Function for reception login reception parol
def librus_login(message):
    # logging.info("connect to function 'librus_login'.  Request/responce login")
    print("connect to function 'librus_login'.  Request/responce login")
    msg_parol = bot.send_message(
            message.chat.id, replicas["librus parol"])
    data_list.extend((message.chat.id, message.text))
    bot.register_next_step_handler(msg_parol, librus_parol)


# Function for reactions for connect to Librus
def librus_parol(message):
    # logging.info("connect to function 'librus_parol'.  Request/responce parol. To write id_chat, login, parol to DB")
    print("connect to function 'librus_parol'.  Request/responce parol. To write id_chat, login, parol to DB")
    msg_sucess = bot.send_message(
            message.chat.id, replicas["librus success"]+data_list[1]+","+message.text+replicas["permission_librus"])
    data_list.append(message.text)
    # logging.info("Append login. parol. id to list. Sucess")
    print("Append login. parol. id to list. Sucess")
    dict_secret[data_list.pop(0)] = data_list
    with open('data.json', 'w') as outfile:
        json.dump(dict_secret, outfile)
    # logging.info(" to write json in file is success")
    print(" to write json in file is success")
    bot.register_next_step_handler(msg_sucess, librus_connect)


def librus_connect(message):
    # logging.info("connect to function 'librus_connect'. Start work")
    print("connect to function 'librus_connect'. Start work")
    queue_work()


def reqest_work()->None:
    with open('data.json') as f:
        secret = json.load(f)
    print("success download json file")
    # the list of id user in chat
    id_user = tuple(secret.keys())
    work_ = librus_ads(secret)
    for is_data in id_user:
        bot.send_message(is_data, work_, parse_mode="html")




work = schedule.every().day.at("16:00").do(reqest_work)

def run():
    # logging.info("Start bot")
    print("start bot")
    bot.infinity_polling()
#
#
if __name__ == '__main__':
  run()


# # # Функция, обрабатывающая команду /stop
# # @bot.message_handler(commands = ["stop"])
# # def stopbot(message):
# #     send = bot.send_message(message.chat.id,replicas["stop"]+ message.chat.first_name)
# #     # print(message.chat.first_name)
# #     # print(message)
# #     bot.register_next_step_handler(send, requestdate)
#
#
# #     # Получение сообщений от юзера
# # @bot.message_handler(content_types=["text"])
# # def handle_text(message):
# #     bot.send_message(message.chat.id, 'Вы написали: ' + message.text)


