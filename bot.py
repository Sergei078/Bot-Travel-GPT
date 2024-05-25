from config import TOKEN
import telebot
import random
from buttons import menu_key, vbord_key, geo_key, verno_key, choice_key, wheather_key, city_info_key, create_keyboard, translate_key
from Weather_function import getting_the_weather, getting_the_weather_tomorrow, getting_the_weather_five_day
from geoloc import i_know_where_you_live, you_know_where_you_live
from Gpt import yandex_gpt_beautiful_presentation_of_information, yandex_gpt_clothes, yandex_gpt_nature_features, yandex_gpt_interesting_facts, yandex_gpt_attractions_city
import logging
from database import create_database, add_message, update_city, select_city, select_token, update_token


logging.basicConfig(filename='logConfig.log', encoding='utf-8', level=logging.WARNING,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s")
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

developer = ["https://t.me/ild1kpy", "https://t.me/ArtemSav5", "https://t.me/SergeiDobrynkin07",
             "https://t.me/Programist337)", "https://t.me/matvejkazxc"]


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user_id = message.from_user.id
        base = create_database()
        if not base:
            create_database()
            add_message(user_id)
        city = select_city(user_id)
        if city is None or city == '':
            bot.send_message(message.chat.id, '<b>Для работы с ботом 🤖\n'
                                              'нужно определить город!</b>', reply_markup=verno_key(),
                             parse_mode='HTML')
            return
        bot.send_message(message.chat.id, f'<b>Здравствуй, друг👋\n\n</b>'
                                          '<i>Я полезный ассистент,\n'
                                          'который всегда готов\n'
                                          'сопровождать вас в \n'
                                          'ваших путешествиях✈️. \n\n'
                                          '<b>Чем я могу помочь?</b>\n'
                                          'Помогу вам собрать всю \n'
                                          'необходимую информацию \n'
                                          'города, куда держите путь,\n'
                                          'и даже подскажу как \n'
                                          'одеться👖 по погоде.</i>\n\n'
                                          '<b>Бот работает на YaGPT3🔮,\n'
                                          'самой новейшей модели у\n'
                                          '<u>Яндекса</u>.</b>\n\n'
                                          '<b>Нужна помощь - /help</b>', parse_mode='HTML', reply_markup=menu_key())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Погода в городе🌩')
def weather(message):
    try:
        bot.send_message(message.chat.id, 'Выбери что нужно:', reply_markup=wheather_key(), parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Перевод📝')
def translate(message):
    try:
        bot.send_message(message.chat.id, 'Выбери что нужно:', reply_markup=translate_key(), parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Информация о городе🌍')
def city_info(message):
    try:
        bot.send_message(message.chat.id, 'Выберите что нужно:', reply_markup=city_info_key(), parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text in ['Выбрать город🌍', 'Перевыбрать город🌍'])
def choise_city(message):
    try:
        user_id = message.from_user.id
        base = create_database()
        if not base:
            create_database()
            add_message(user_id)
        bot.send_message(message.chat.id, '<b>Выберите каким способом\n'
                                          'вы хотите добавить город:</b>', reply_markup=vbord_key(), parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Написать город🌍')
def city_text(message):
    try:
        bot.send_message(message.chat.id, '<b>Напиши название города</b>\n\n'
                                          '<i>Не забудь проверить на \n'
                                          'правильность написания!</i>\n', parse_mode='HTML')
        bot.register_next_step_handler(message, city_text_to_city)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


def city_text_to_city(message):
    try:
        user_id = message.from_user.id
        city = message.text
        location = you_know_where_you_live(city)
        bot.send_message(message.chat.id, f'<b>Ваш город:</b> \n<i>{location}</i>\n\n'
                                          f'<b>Данные верные?</b>', reply_markup=choice_key(), parse_mode='HTML')
        update_city(city, user_id)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.callback_query_handler(func=lambda callback: callback.data == 'Yes')
def city_yes(callback):
    try:
        user_id = callback.message.chat.id
        city = select_city(user_id)
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, f'<b>Ваш город: {city} </b>\n\n'
                                                   f'<i>Успешно сохранен✅</i>', reply_markup=menu_key(),
                         parse_mode='HTML')
    except Exception as e:
        bot.send_message(callback.message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.callback_query_handler(func=lambda callback: callback.data == 'No')
def city_no(callback):
    try:
        bot.answer_callback_query(callback.id)
        user_id = callback.message.chat.id
        update_city('', user_id)
        city = select_city(user_id)
        if city is None or city == '':
            bot.send_message(callback.message.chat.id, 'Попробуйте еще раз', reply_markup=vbord_key())
            bot.register_next_step_handler(callback.message, choise_city)
            return
        bot.send_message(callback.message.chat.id, 'Возвращаю в меню', reply_markup=menu_key())
    except Exception as e:
        bot.send_message(callback.message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Найти на карте🗺')
def city_geo(message):
    try:
        bot.send_message(message.chat.id, '<b>Чтобы отправить локацию\n'
                                          'города, следуйте этой\n'
                                          'инструкции:</b>\n\n'
                                          '<i>1. Нажмите на вашей\n'
                                          'клавиатуре <b>скрепку📎</b>,\n'
                                          'вам откроется меню.\n'
                                          '2. В меню выберите \n'
                                          '<b>"Геопозиция"</b>\n'
                                          '3. Появится карта, на ней\n'
                                          'нужно найти тот город,\n'
                                          'куда отправляетесь.</i>\n\n'
                                          '<u>Примечание:</u>\n'
                                          '<i>Если хотите узнать про\n'
                                          'свой город, то не нужно\n'
                                          'никуда переходить, просто\n'
                                          'нажмите на кнопку \n'
                                          '<b>Отправить свою локацию📍</b></i>\n\n'
                                          '<b>На телефоне должна быть\n'
                                          'включена геолокация❗️</b>\n', reply_markup=geo_key(),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, city_geo_to_city)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


def city_geo_to_city(message):
    try:
        user_id = message.from_user.id
        Location = message.location
        if not Location:
            bot.send_message(message.chat.id, 'Не могу прочитать.\n'
                                              'Возвращаю в начало', reply_markup=verno_key())
            return
        lat = Location.latitude
        long = Location.longitude
        city, country = i_know_where_you_live(lat, long)
        if city == 'городской округ Курск':
            city = 'Курск'
        update_city(city, user_id)
        bot.send_message(message.chat.id, f'<b>Ваш город: {city}, {country} </b>\n\n'
                                          f'<i>Успешно сохранен✅</i>', reply_markup=menu_key(), parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Перевод текста📝')
def translate_fun(message):
    try:
        bot.send_message(message.chat.id, 'Напишите текст:')
        bot.register_next_step_handler(message, translate_text)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


def translate_text(message):
    try:
        text = message.text
        user_id = message.from_user.id

        bot.send_message(message.chat.id, 'Теперь выбери язык', reply_markup=create_keyboard(
            ['🇨🇳', '🇬🇧', '🇧🇾', '🇩🇪', '🇪🇸', '🇪🇪', '🇫🇷', '🇯🇵', '🇵🇹', '🇷🇴', '🇰🇿']))
        bot.register_next_step_handler(message, translate_lang)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


def translate_lang(message):
    try:
        text = ''
        bot.send_message(message.chat.id, f'Ваш перевод: {text}', reply_markup=menu_key())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Погода на сегодня🌦')
def wheather(message):
    try:
        message_user = bot.send_message(message.chat.id, 'Ожидайте ответа...')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️Обратитесь к разработчикам "/contacts"', reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        wheather1 = getting_the_weather(city)
        wheather_gpt_info = yandex_gpt_beautiful_presentation_of_information(city, wheather1[0], wheather1[1], wheather1[2],
                                                                             wheather1[3])
        use_token = len(wheather_gpt_info)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=wheather_gpt_info, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Погода на завтра🌥')
def wheather_tomorrow(message):
    try:
        message_user = bot.send_message(message.chat.id, 'Ожидайте ответа...')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️Обратитесь к разработчикам "/contacts"', reply_markup=menu_key())
            return
        tomorrow = getting_the_weather_tomorrow(city)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=tomorrow, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)

@bot.message_handler(func=lambda message: message.text == 'Погода на 5 дней🌧')
def week_wheather(message):
    message_user = bot.send_message(message.chat.id, 'Ожидайте ответа...')
    user_id = message.from_user.id
    city = select_city(user_id)
    if city is None or city == '':
        bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
        return
    week = getting_the_weather_five_day(city)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                          text=week, parse_mode='markdown')

@bot.message_handler(func=lambda message: message.text == 'Совет по одежде👕')
def clothes(message):
    try:
        message_user = bot.send_message(message.chat.id, 'Ожидайте ответа...')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️Обратитесь к разработчикам "/contacts"', reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        info_wheather = getting_the_weather(city)
        clothe = yandex_gpt_clothes(info_wheather[0], info_wheather[1], info_wheather[2], info_wheather[3])
        use_token = len(clothe)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=clothe, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Особенности природы🏞')
def nature_facts(message):
    try:
        message_user = bot.send_message(message.chat.id, 'Ожидайте ответа...')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️Обратитесь к разработчикам "/contacts"', reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        nature = yandex_gpt_nature_features(city)
        use_token = len(nature)
        use_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=nature, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Интересные факты💡')
def facts(message):
    try:
        message_user = bot.send_message(message.chat.id, 'Ожидайте ответа...')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️Обратитесь к разработчикам "/contacts"', reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        fact = yandex_gpt_interesting_facts(city)
        use_token = len(fact)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=fact, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Достопримечательности🗺')
def attractions(message):
    try:
        message_user = bot.send_message(message.chat.id, 'Ожидайте ответа...')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️Обратитесь к разработчикам "/contacts"', reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        attraction = yandex_gpt_attractions_city(city)
        use_token = len(attraction)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=attraction, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())


@bot.message_handler(commands=['contacts'])
def contacts(message):
    try:
        random_develop = random.choice(developer)
        bot.send_message(message.chat.id, f'Свяжись с [создателем]({random_develop})',
                         parse_mode='Markdown', )
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Вернуться в меню🔙')
def back_menu(message):
    try:
        bot.send_message(message.chat.id, 'Возвращаемся в меню...', reply_markup=menu_key())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(commands=['help'])
def Help(message):
    try:
        bot.send_message(message.chat.id, f'<b>/start</b> - <i>Перезапустить бота</i>\n'
                                          f'<b>/contacts</b> - <i>Связь с создателями</i>\n'
                                          f'<b>/help</b> - <i>Помощь</i>', reply_markup=menu_key(), parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(commands=['log'])
def log(message):
    try:
        with open("logs.log", "rb") as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: True)
def unknown(message):
    user_id = message.from_user.id
    base = create_database()
    city = select_city(user_id)
    if not base:
        create_database()
        add_message(user_id)
    if city == '':
        bot.send_message(message.chat.id, 'Пользуйтесь кнопками!')
        bot.send_message(message.chat.id, 'У вас не выбран город❗️', reply_markup=verno_key())
        return
    bot.send_message(message.chat.id, 'Извините, я вас не понимаю.', reply_markup=menu_key())


bot.polling(none_stop=True)
