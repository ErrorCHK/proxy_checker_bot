import logging
import time
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv,find_dotenv

from keyboards import button_check,button_list,button_end
from check_proxy import get_check_proxy


storage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot,storage=storage)


class Form(StatesGroup):
    type_proxy = State()
    count_proxy = State()


@dp.message_handler(state='*', commands='🔙')
@dp.message_handler(lambda x: x.text == '🔙', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.reset_data()
    await message.answer('Select type proxy.', reply_markup=button_check)
    await Form.type_proxy.set()
    
    

@dp.message_handler(commands=['start'])
async def send_welcome(message : types.Message):
    await message.answer('Hello. I can check you proxy. Type: HTTP/SOCKs5',reply_markup=button_check)
    await Form.type_proxy.set()

    
### Message handlers HTTP or SOCKS5
@dp.message_handler(lambda c: c.text in ['🌐 Check HTTP','🌐 Check SOCKs5'],state=Form.type_proxy)
async def type_proxy(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type_proxy'] = message.text
        await Form.next()
        await message.answer('Select count proxy. By one or List',reply_markup=button_list)
        
@dp.message_handler(lambda c: c.text in ['📥 By one','📚 List'],state=Form.count_proxy)
async def count_proxy(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count_proxy'] = message.text
        await Form.next()
        await message.answer(f'<b>You have selected.</b>\n ✅TYPE: <b>{data["type_proxy"].split()[-1]}</b>\n\
👉Count: {data["count_proxy"]}\n<b>Enter proxy by template</b>\n \
login:password@ip:port',reply_markup=types.ReplyKeyboardRemove())



### Message handlers enter proxy and check
@dp.message_handler(lambda x: '@' in x.text)
async def check_proxy(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            if data["count_proxy"] == '📥 By one':
                status = get_check_proxy(data["type_proxy"],message.text)
                await message.answer_location(status[1][0],status[1][1])
                await message.answer(status[0])
            elif data['count_proxy'] == '📚 List':
                for proxy in message.text.split('\n'):
                    time.sleep(6) #without time.sleep() API blocking requests.
                    status = get_check_proxy(data["type_proxy"],proxy)
                    if not isinstance(status,tuple):
                        await message.answer(f'{status} - {proxy.split("@")[1]}')
                    else:
                        await message.answer_location(status[1][0],status[1][1])
                        await message.answer(status[0])     
            else:
                await message.answer('❌Type proxy not supported❌\n<b>Enter proxy by template</b>\n \
login:password@ip:port')
        await message.answer('I\'m waiting for more proxies...',reply_markup=button_end)
        

    except LookupError:
         await message.answer('You have incorrectly selected the number of proxies to check\nStart again 🔙 ',reply_markup=button_end)   
    except Exception:
         await message.answer('Everything is broken. Start again. 🔜 /start')
        
        

@dp.message_handler(content_types=['text'])
async def send_error(message: types.Message):
    await message.answer('💁🏻‍♂️ I don\'t understand, please click /start')
    
    

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)
