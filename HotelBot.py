import datetime
import telebot
import Configuration as c
from booking_api_to_kafka import *

bot = telebot.TeleBot(c.telegram_token)
@bot.message_handler(commands=['start', 'help'])
def send_first(message):
    print(message.from_user.username)
    msg =f'''Hi {message.from_user.username}! wellcome to the HotelBot
please type city, checkin date, check out date, room number and adult number for your vacation
please seperate them by comma.
For example: london, 2023-05-01, 2023-05-03, 2, 2'''
    bot.send_message(message.chat.id, msg, parse_mode= 'Markdown')

#get variables for each user

def booking_api_response(message):
    params_arr = message.text.split(",")
    city = params_arr[0]
    checkin_date = params_arr[1].strip()
    checkout_date = params_arr[2].strip()
    room_number = params_arr[3].strip()
    adult_number = params_arr[4].strip()
    if(isValid(checkin_date,checkout_date)):
        chat_id = message.chat.id
        user_id = message.from_user.id
        dest_id_arr = request_location(city)
        if dest_id_arr != 0:
            booking_url = request_hotels(dest_id_arr, room_number, checkin_date, checkout_date, adult_number,user_id,chat_id)
            print(booking_url)
# show the list of booking hotel to each user
            for row_book in (range(len(booking_url))):
                bot.send_message(message.chat.id, booking_url[row_book])
# prob with api - independent testing on tge api
        else:
            bot.send_message(message.chat.id, "The city does not exist, please type again")
    else:
        bot.send_message(message.chat.id, "the date is not valid, please type again")

def isValid(checkin_date,checkout_date):
    try:
        ch_in_date = datetime.datetime.strptime(checkin_date, '%Y-%m-%d')
        ch_out_date = datetime.datetime.strptime(checkout_date, '%Y-%m-%d')
        current_time = datetime.datetime.today()
        current_time = current_time.strftime('%Y-%m-%d')
        current_time = datetime.datetime.strptime(current_time, '%Y-%m-%d')
        if ch_in_date >= current_time and ch_out_date >= current_time and ch_out_date >= ch_in_date:
            return True
        else:
            return False
    except ValueError as e:
        print('ValueError:', e)

@bot.message_handler(func=booking_api_response)
def foo(message):
    pass

bot.infinity_polling()

