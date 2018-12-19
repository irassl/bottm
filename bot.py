# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mydatabase import *
from sqlalchemy.orm import sessionmaker

TOKEN='TOKEN'
REQUEST_KWARGS={
    'proxy_url': 'socks5://104.248.255.135:1080'
    # Optional, if you need authentication:

}
updater = Updater(TOKEN,request_kwargs=REQUEST_KWARGS)
Session= sessionmaker()
Session.configure(bind=engine)
session = Session()
dispatcher = updater.dispatcher
# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
    querry = User(update.message.chat_id,update.message.from_user.username,update.message.date)
    session.add(querry)


    session.commit()
def textMessage(bot, update):
    #response = 'Получил Ваше сообщение: ' + update.message.text
    #bot.send_message(chat_id=update.message.chat_id, text=response)
    querry = Messages(update.message.chat_id, update.message.text, last_message=False)
    session.add(querry)

def writeCommand(bot,update):
    #session.commit()
    querry = session.query(Messages).filter(Messages.user_id==update.message.chat_id).all()
    for row in querry:
        row.last_message = False
        session.add(row)
    last = querry[-1]
    last.last_message = True
    session.add(last)
    session.commit()
    bot.send_message(chat_id=update.message.chat_id, text=last.id)

def read_lastCommand(bot,update):
    querry = session.query(Messages).filter(Messages.user_id==update.message.chat_id).filter_by(last_message=True).first()
    bot.send_message(chat_id=update.message.chat_id,text=querry.message_text)
def readCommand(bot,update):
    #session.rollback()
    a = (update.message.text).split(' ')
    querry = session.query(Messages).filter(Messages.id == a[-1]).first()
    if querry == None:
       bot.send_message(chat_id=update.message.chat_id, text='sorry')
    else:
        bot.send_message(chat_id=update.message.chat_id, text=querry.message_text)

def readallCommand(bot,update):
    #session.rollback()
    querry = session.query(Messages).filter(Messages.user_id == update.message.chat_id).all()
    list1 = []
    for row in querry:
        list1.append(row.message_text)
    bot.send_message(chat_id=update.message.chat_id, text=(', '.join(list1)))



# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
write_command_handler = CommandHandler('write',writeCommand)
readlast_command_handler= CommandHandler('read_last',read_lastCommand)
read_command_handler=CommandHandler('read',readCommand)
readall_command_handler = CommandHandler('readall',readallCommand)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(write_command_handler)
dispatcher.add_handler(readlast_command_handler)
dispatcher.add_handler(read_command_handler)
dispatcher.add_handler(readall_command_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()