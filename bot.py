import random

import requests
import telebot
from telebot import types

from buttons import (choice_key, city_info_key, create_keyboard, geo_key,
                     menu_key, vbord_key, verno_key, weather_clothes_key,
                     wheather_key)
from config import DEVELOPER, TOKEN
from database import (add_message, create_database, select_city, select_token,
                      select_translate, update_city, update_token,
                      update_translate)
from fhoto_city import get_place
from geoloc import i_know_where_you_live, you_know_where_you_live
from Gpt import (yandex_gpt_attractions_city,
                 yandex_gpt_beautiful_presentation_of_information,
                 yandex_gpt_brief_retelling, yandex_gpt_clothes,
                 yandex_gpt_interesting_facts, yandex_gpt_nature_features)
from log import logger
from translate import translater
from Weather_function import (getting_the_weather,
                              getting_the_weather_five_day,
                              getting_the_weather_tomorrow)

bot = telebot.TeleBot(TOKEN)


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


@bot.message_handler(func=lambda message: message.text == 'Раздел погоды⛅️')
def weather(message):
    try:
        bot.send_message(message.chat.id, '<b>Выберите какую \n'
                                          'информацию вы хотите \n'
                                          'получить о погоде:</b>', reply_markup=wheather_key(), parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Раздел о городе🌆')
def city_info(message):
    try:
        bot.send_message(message.chat.id, '<b>Выберите какую \n'
                                          'информацию вы хотите \n'
                                          'получить о городе:</b>', reply_markup=city_info_key(), parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Фото📸')
def photo_city_user_message(message):
    try:
        user_id = message.from_user.id
        city = select_city(user_id)
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        photo = get_place(city.lower())
        if photo in ['для вашего города нет информации', 'ошибка поиска мест', 'что то пошло не так']:
            bot.send_message(message.chat.id, 'Для твоего города не\n'
                                              'нашлось фотографий, \n'
                                              'ознакомься с актуальным\n'
                                              'списком городов. /city')
            return
        name, description, address, img_source = photo
        img_data = requests.get(img_source).content
        with open('image_name.jpg', 'wb') as handler:
            handler.write(img_data)
        with open('image_name.jpg', 'rb') as file:
            f = file.read()
        bot.send_photo(message.chat.id, photo=f, caption=f'<b>Имя:</b> <i>{name}</i>\n\n'
                                                         f'<b>Описание:</b> <i>{description}</i>\n\n'
                                                         f'<b>Адрес:</b> <i>{address}</i>', parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Кратко пересказать✏')
def a_brief_retelling_message(message):
    try:
        bot.send_message(message.chat.id, '<b>Вставь сюда текст:</b>\n\n'
                                          '<b><u>Для чего это нужно?</u></b>\n'
                                          '<i>Например в нашем боте,\n'
                                          'есть очень много \n'
                                          'информации о городе, если \n'
                                          'вам некогда все это читать, \n'
                                          'на помощь придет краткий \n'
                                          'пересказ,просто скопируйте \n'
                                          'и вставьте текст.</i>', reply_markup=types.ReplyKeyboardRemove(),
                         parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)

    def text_user(message):
        try:
            message_user = bot.send_message(message.chat.id, '⏳')
            user_id = message.from_user.id
            text = message.text
            user_token = select_token(user_id)
            if user_token <= 0:
                bot.send_message(message.chat.id, 'Токены потрачены❗️\n'
                                                  'Обратитесь к разработчикам\n'
                                                  '/contacts',
                                 reply_markup=menu_key())
                return
            text_gpt = yandex_gpt_brief_retelling(text)
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                                  text=text_gpt, parse_mode='markdown')
            bot.send_message(message.chat.id, 'Возвращаю в меню...', reply_markup=menu_key())
            use_token = len(text_gpt)
            user_token -= use_token
            update_token(user_id, user_token)
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
            logger.error(e)

    bot.register_next_step_handler(message, text_user)


@bot.message_handler(func=lambda message: message.text in ['Выбрать город🌍', 'Перевыбрать город🌍'])
def choice_city_message(message):
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
def city_text_message(message):
    try:
        bot.send_message(message.chat.id, '<b>Напиши название города</b>\n\n'
                                          '<i>Не забудь проверить на \n'
                                          'правильность написания!</i>\n', parse_mode='HTML')
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

    bot.register_next_step_handler(message, city_text_to_city)


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
            bot.register_next_step_handler(callback.message, choice_city_message)
            return
        bot.send_message(callback.message.chat.id, 'Возвращаю в меню', reply_markup=menu_key())
    except Exception as e:
        bot.send_message(callback.message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Переводчик🇬🇧')
def translate_fun_message(message):
    try:
        bot.send_message(message.chat.id, 'Напишите текст для\n'
                                          'перевода:', reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)

    def translate_text(message):
        try:
            text = message.text
            user_id = message.from_user.id
            update_translate(text, user_id)
            bot.send_message(message.chat.id, '<b>Теперь выбери язык:</b>\n'
                                              '🇷🇺 - Россия\n'
                                              '🇬🇧 - Английский\n'
                                              '🇧🇾 - Беларусь\n'
                                              '🇩🇪 - Германия\n'
                                              '🇪🇸 - Испания\n'
                                              '🇪🇪 - Эстония\n'
                                              '🇫🇷 - Франция\n'
                                              '🇯🇵 - Япония\n'
                                              '🇵🇹 - Португалия\n'
                                              '🇷🇴 - Румыния\n'
                                              '🇰🇿 - Казахстан\n',
                             reply_markup=create_keyboard(
                                 ['🇷🇺', '🇬🇧', '🇧🇾', '🇩🇪', '🇪🇸', '🇪🇪', '🇫🇷', '🇯🇵', '🇵🇹', '🇷🇴', '🇰🇿']), parse_mode='html')
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
            logger.error(e)

    bot.register_next_step_handler(message, translate_text)


@bot.message_handler(
    func=lambda message: message.text in ['🇷🇺', '🇨🇳', '🇬🇧', '🇧🇾', '🇩🇪', '🇪🇸', '🇪🇪', '🇫🇷', '🇯🇵', '🇵🇹', '🇷🇴', '🇰🇿'])
def translate_lang_message(message):
    try:
        lang = message.text
        user_id = message.from_user.id
        e = select_translate(user_id)
        text = translater(e, lang)
        bot.send_message(message.chat.id, f'<b>Ваш перевод:</b> \n<i>{text}</i>\n\n'
                                          f'<b>Изначальный текст:</b>\n'
                                          f'<i>{e}</i>', reply_markup=menu_key(), parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Найти на карте🗺')
def city_geo_message(message):
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
            update_city(city, user_id)
            bot.send_message(message.chat.id, f'<b>Ваш город: {city}, {country} </b>\n\n'
                                              f'<i>Успешно сохранен✅</i>', reply_markup=menu_key(), parse_mode='HTML')
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
            logger.error(e)

    bot.register_next_step_handler(message, city_geo_to_city)


@bot.message_handler(func=lambda message: message.text == 'На завтра⛈')
def weather_tomorrow_message(message):
    try:
        message_user = bot.send_message(message.chat.id, '⏳')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️\n'
                                              'Обратитесь к разработчикам\n'
                                              '"/contacts"\n',
                             reply_markup=menu_key())
            return
        tomorrow = getting_the_weather_tomorrow(city)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=tomorrow, parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'На 5 дней🔮')
def week_weather_message(message):
    message_user = bot.send_message(message.chat.id, '⏳')
    user_id = message.from_user.id
    city = select_city(user_id)
    if city is None or city == '':
        bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
        return
    week = getting_the_weather_five_day(city)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                          text=week, parse_mode='html')


@bot.message_handler(func=lambda message: message.text == 'Погода сейчас⛱')
def weather_message(message):
    try:
        message_user = bot.send_message(message.chat.id, '⏳')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️\n'
                                              'Обратитесь к разработчикам\n'
                                              '"/contacts"\n',
                             reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        weather = getting_the_weather(city)
        weather_gpt = yandex_gpt_beautiful_presentation_of_information(city, weather[0], weather[1], weather[2],
                                                                       weather[3])
        use_token = len(weather_gpt)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=weather_gpt, parse_mode='markdown', reply_markup=weather_clothes_key())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.callback_query_handler(func=lambda callback: callback.data == 'clothes')
def clothes_callback(callback):
    try:
        message_user = bot.send_message(callback.message.chat.id, '⏳')
        bot.answer_callback_query(callback.id)
        user_id = callback.message.chat.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(callback.message.chat.id, 'Токены потрачены❗️\n'
                                                       'Обратитесь к разработчикам\n'
                                                       '"/contacts"\n',
                             reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(callback.message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        wheather = getting_the_weather(city)
        clothes = yandex_gpt_clothes(wheather[0], wheather[1], wheather[2], wheather[3])
        use_token = len(clothes)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=message_user.message_id,
                              text=clothes, parse_mode='markdown')
    except Exception as e:
        bot.send_message(callback.message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Природа🏞')
def forest_message(message):
    try:
        message_user = bot.send_message(message.chat.id, '⏳')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️\n'
                                              'Обратитесь к разработчикам\n'
                                              '"/contacts"\n',
                             reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        forest = yandex_gpt_nature_features(city)
        use_token = len(forest)
        use_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=forest, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Факты💡')
def facts_message(message):
    try:
        message_user = bot.send_message(message.chat.id, '⏳')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️\n'
                                              'Обратитесь к разработчикам\n'
                                              '"/contacts"\n',
                             reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        facts = yandex_gpt_interesting_facts(city)
        use_token = len(facts)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=facts, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Достопримечательности🗺')
def attractions_message(message):
    try:
        message_user = bot.send_message(message.chat.id, '⏳')
        user_id = message.from_user.id
        city = select_city(user_id)
        user_token = select_token(user_id)
        if user_token <= 0:
            bot.send_message(message.chat.id, 'Токены потрачены❗️\n'
                                              'Обратитесь к разработчикам\n'
                                              '"/contacts"\n',
                             reply_markup=menu_key())
            return
        if city is None or city == '':
            bot.send_message(message.chat.id, 'Не выбран город❗️', reply_markup=menu_key())
            return
        attractions = yandex_gpt_attractions_city(city)
        use_token = len(attractions)
        user_token -= use_token
        update_token(user_id, user_token)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_user.message_id,
                              text=attractions, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())


@bot.message_handler(commands=['contacts'])
def contacts_commands(message):
    try:
        random_develop = random.choice(DEVELOPER)
        bot.send_message(message.chat.id, f'Свяжись с [создателем]({random_develop})',
                         parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(func=lambda message: message.text == 'Меню↩️')
def back_menu_message(message):
    try:
        bot.send_message(message.chat.id, 'Возвращаемся в меню...', reply_markup=menu_key())
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(commands=['help'])
def help_commands(message):
    try:
        bot.send_message(message.chat.id, f'<b>/start</b> - <i>Перезапустить бота</i>\n'
                                          f'<b>/contacts</b> - <i>Связь с создателями</i>\n'
                                          f'<b>/help</b> - <i>Помощь</i>\n'
                                          f'<b>/city</b> - <i>Доступные города</i>\n'
                                          f'<b>/manual</b> - <i>Инструкция бота</i>', reply_markup=menu_key(),
                         parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=verno_key())
        logger.error(e)


@bot.message_handler(commands=['log'])
def log_commands(message):
    try:
        with open("logs.log", "rb") as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(commands=['city'])
def log_commands(message):
    try:
        bot.send_message(message.chat.id, '<b>Список доступных городов:</b>\n'
                                          '<i>Санкт-Петербург</i>\n'
                                          '<i>Москва</i>\n'
                                          '<i>Новосибирск</i>\n'
                                          '<i>Екатеринбург</i>\n'
                                          '<i>Нижний Новгород</i>\n'
                                          '<i>Казань</i>\n'
                                          '<i>Выборг</i>\n'
                                          '<i>Красноярск</i>\n', parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(commands=['manual'])
def manual_commands(message):
    try:
        message_text = (
            "Привет! Вот краткое руководство по кнопкам интерфейса:\n\n"
            "<b>Раздел о городе🌆:</b>\n<i>Получите информацию о городе, включая достопримечательности, интересные факты и природу.</i>\n\n"
            "<b>Раздел погоды⛅️:</b>\n<i>Узнайте текущую погоду, прогноз на завтра или на пять дней вперед. Получите советы по одежде, чтобы не попасть под дождь!</i>\n\n"
            "<b>Переводчик🇬🇧:</b>\n<i>Используйте для перевода текстов на другие языки.</i>\n\n"
            "<b>Кратко пересказать✏:</b>\n<i>Получите краткое содержание длинных текстов.</i>\n\n"
            "<b>Перевыбрать город🌍:</b>\n<i>Измените текущий город, используя поиск на карте или написание названия города.</i>\n\n"
            "<b>Фото📸:</b>\n<i>Отправляет фото достопримечательности.</i>\n\n"
            "<b>Используйте эти кнопки для более удобной навигации и получения нужной информации. Приятного использования!</b>"
        )
        bot.send_message(message.chat.id, message_text, parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка❗️{e}', reply_markup=menu_key())
        logger.error(e)


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
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
