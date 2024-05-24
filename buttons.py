from telebot import types


def menu_key():
    markup_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = types.KeyboardButton("Информация о городе🌍")
    button_2 = types.KeyboardButton("Погода в городе🌩")
    button_3 = types.KeyboardButton("Профиль👤")
    button_4 = types.KeyboardButton("Перевод📝")
    button_5 = types.KeyboardButton("Перевыбрать город🌍")
    markup_menu.add(button_2)
    markup_menu.add(button_1, button_3)
    markup_menu.add(button_4, button_5)
    return markup_menu

def city_info_key():
    markup_info = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_3 = types.KeyboardButton("Особенности природы🏞")
    button_6 = types.KeyboardButton("Интересные факты💡")
    button_5 = types.KeyboardButton("Достопримечательности🗺")
    button_4 = types.KeyboardButton("Вернуться в меню🔙")
    button_1 = types.KeyboardButton("Совет по одежде👕")
    markup_info.add(button_3, button_4)
    markup_info.add(button_1, button_6)
    markup_info.add(button_5)
    return markup_info

def translate_key():
    markup_translate = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = types.KeyboardButton("Перевод текста📝")
    button_2 = types.KeyboardButton("Вернуться в меню🔙")
    markup_translate.add(button_1, button_2)
    return markup_translate
def wheather_key():
    markup_wheather = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = types.KeyboardButton("Погода на сегодня🌦")
    button_2 = types.KeyboardButton("Погода на завтра🌥")
    button_3 = types.KeyboardButton("Погода на 5 дней🌧")
    button_4 = types.KeyboardButton("Вернуться в меню🔙")
    markup_wheather.add(button_1, button_2, button_3, button_4)
    return markup_wheather
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

def create_keyboard(buttons_list):
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

def choice_key():
    markup_vb2 = types.InlineKeyboardMarkup(row_width=2)
    button_vb = types.InlineKeyboardButton("Нет❌", callback_data='No')
    button_vb1 = types.InlineKeyboardButton("Да✅", callback_data='Yes')
    markup_vb2.add(button_vb1, button_vb)
    return markup_vb2
