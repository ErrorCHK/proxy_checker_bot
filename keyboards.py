from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

check_http = KeyboardButton('🌐 Check HTTP')
check_socks5 = KeyboardButton('🌐 Check SOCKs5')
button_check = ReplyKeyboardMarkup(resize_keyboard=True)
button_check.add(check_http,check_socks5)

by_one = KeyboardButton('📥 By one')
lists = KeyboardButton('📚 List')
button_list = ReplyKeyboardMarkup(resize_keyboard=True)
button_list.add(by_one,lists)

end = KeyboardButton('🔙')
button_end = ReplyKeyboardMarkup(resize_keyboard=True)
button_end.add(end)