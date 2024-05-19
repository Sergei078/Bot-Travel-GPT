from telebot import types


def menu_key():
    markup_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_2 = types.KeyboardButton("Начать путешествие ✈️ ")
    markup_menu.add(button_2)
    return markup_menu


def inline_key():
    markup_in = types.InlineKeyboardMarkup(row_width=1)
    inline_button_1 = types.InlineKeyboardButton("Что одеть? 👕", callback_data="weather")
    inline_button_2 = types.InlineKeyboardButton("Особенности города 🏡", callback_data="city_peculiarities")
    markup_in.add(inline_button_1, inline_button_2)
    return markup_in


def geo_key():
    markup_geo = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_geo = types.KeyboardButton("Задать местоположение📍", requests_location=True)
    markup_geo.add(button_geo)
    return markup_geo
