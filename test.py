from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json




TOKEN = '1890561220:AAE0_UyC7VsyoqjcUbVeGoigbdMsnyatu3M'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dam = InlineKeyboardMarkup()
dam.add(InlineKeyboardButton('check',callback_data='hota'))

numbers = '1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟'.split(' ')

@dp.message_handler()
async def efw(message:types.Message):
    await message.answer('hello',reply_markup=dam)


@dp.callback_query_handler()
async def ewfw(message:types.CallbackQuery):
    cuta = InlineKeyboardMarkup()
    url = 'https://api.coincap.io/v2/assets'
    r = requests.get(url)
    data = json.loads(r.text)

    categories = [[numbers[int(i['rank'])-1]+' '+i["symbol"] if len(numbers[int(i['rank'])-1]+' '+i["symbol"])==8 else numbers[int(i['rank'])-1]+'    '+i["symbol"],'💲'+i['priceUsd'][:5] if int(float(i['priceUsd'][:7])) < 2 else ('💲'+i['priceUsd'][:7] if int(float(i['priceUsd'][:7])) < 999 else '💲'+(str(int(float(i['priceUsd'][:7])))[::-1][:3]+','+str(int(float(i['priceUsd'][:7])))[::-1][3:])[::-1]+'.'+i['priceUsd'][:7][::-1].split('.')[0][::-1] ),'〽️'+str(int(float(i['changePercent24Hr'][:5])))+'.'+i['changePercent24Hr'][:5].split('.')[1][:2]+' %' if '-' in str(i['changePercent24Hr'][:5]) else '〽️+'+str(int(float(i['changePercent24Hr'][:5])))+'.'+i['changePercent24Hr'][:5].split('.')[1][:2]+' %']  for i in data['data'][:10] ]
    for i in categories:
        print(i[0],len(i[0]))
    for i in categories:
        cuta.add(InlineKeyboardButton(i[0],callback_data='e'),InlineKeyboardButton(i[1],callback_data='e'),InlineKeyboardButton(i[2],callback_data='e'))

    await bot.send_photo(message.from_user.id,open('header6.jpg','rb').read(),reply_markup=cuta)

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)


