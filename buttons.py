from telebot import types


def menu_key():
    markup_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = types.KeyboardButton("Совет по одежде👕")
    button_2 = types.KeyboardButton("Погода🌩")
    button_3 = types.KeyboardButton("Особенности природы🏞")
    button_4 = types.KeyboardButton("Перевыбрать город🌍")
    markup_menu.add(button_2)
    markup_menu.add(button_1, button_3)
    markup_menu.add(button_4)
    return markup_menu


def vbord_key():
    markup_vb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_vb1 = types.KeyboardButton("Написать город🌍")
    button_vb = types.KeyboardButton("Найти на карте🗺")
    markup_vb.add(button_vb, button_vb1)
    return markup_vb


def verno_key():
    markup_verno = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = types.KeyboardButton("Выбрать город🌍")
    markup_verno.add(button_1)
    return markup_verno


def geo_key():
    markup_geo = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_geo = types.KeyboardButton("Отправить свою локацию📍", request_location=True)
    markup_geo.add(button_geo)
    return markup_geo


def choice_key():
    markup_vb2 = types.InlineKeyboardMarkup(row_width=2)
    button_vb = types.InlineKeyboardButton("Нет❌", callback_data='No')
    button_vb1 = types.InlineKeyboardButton("Да✅", callback_data='Yes')
    markup_vb2.add(button_vb1, button_vb)
    return markup_vb2
