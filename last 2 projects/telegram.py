from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3
import asyncio
#####################################
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium import webdriver
###############################
from deep_translator import GoogleTranslator
from aiogram.utils.markdown import link
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
#########################################
import json
import random
import requests




from telegramtwitter import aprona
#@hatatapabot

TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

con = sqlite3.connect('base.db')
cur = con.cursor()

#КНОПКИ
k_b1 = KeyboardButton('💚 Следить')
k_b2 = KeyboardButton('❌ Перестать следить')
k_b3 = KeyboardButton('🔰 Аккаунт')
##################################################

##################################################
k_b7 = KeyboardButton('💳 Купить подписку')
k_b78 = KeyboardButton('Активация промокода')
k_b8 = KeyboardButton('Support')



k_m1 = ReplyKeyboardMarkup(resize_keyboard=True)
k_m1.add(k_b1,k_b2)
k_m1.row(k_b3)

k_m1.row(k_b7)
k_m1.row(k_b78)
k_m1.row(k_b8)





azlf = 'qwertyuiopasdfghjklzxcvbnm0123456789-'



@dp.message_handler(lambda message:  'Support' == message.text)
async def process_start_command(message: types.Message):
    await message.answer('Саппорт - @balanceusdy1')

@dp.message_handler(lambda message:  'Активация промокода' == message.text)
async def process_start_command(message: types.Message):
    if cur.execute(f'''SELECT * FROM base where id='{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''Insert INTO base values (?,?,?,?,?,?,?) ''', (message.from_user.id, 1, '', 0, 0, '', 0))
        con.commit()
    await message.answer('Инструкция: promo (и сам промокод\nПример: promo 1234589484efw)')


@dp.message_handler(lambda message:  'promo' in message.text)
async def process_start_command(message: types.Message):
    if cur.execute(f'''SELECT * FROM base where id='{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''Insert INTO base values (?,?,?,?,?,?,?) ''', (message.from_user.id, 1, '', 0, 0, '', 0))
        con.commit()
    try:
        a = message.text.split(' ')[1]
        if a in cur.execute('''select pro from promo''').fetchall()[0]:
            days,count = cur.execute(f'''select days,count from promo where pro ='{a}' ''').fetchall()[0]
            cur.execute(f'''update base set days = days + '{days}',balance = '{count}',count = '{count}' where id = '{message.from_user.id}' ''')
            con.commit()
            cur.execute(f'''Delete from promo where pro = '{a}' ''')
            con.commit()
            await message.answer('Промокод успешно активирован')
        else:
            await message.answer('Такого промокода нет!')
    except:
        await message.answer('Что то не правильно введено')
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Добро пожаловать!",reply_markup=k_m1)

    if cur.execute(f'''SELECT * FROM base where id='{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''Insert INTO base values (?,?,?,?,?,?,?) ''', (message.from_user.id, 1, '', 0, 0, '', 0))
        con.commit()



@dp.message_handler(lambda message:  '💚 Следить' in message.text)
async def echo_message(message: types.Message):
    if cur.execute(f'''SELECT * FROM base where id='{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''Insert INTO base values (?,?,?,?,?,?,?) ''', (message.from_user.id, 1, '', 0, 0, '', 0))
        con.commit()
    await message.answer('Введите: /follow (никнейм человека)\nПример: /follow elonmusk')


@dp.message_handler(lambda message:  '❌ Перестать следить' in message.text)
async def echo_message(message: types.Message):
    if cur.execute(f'''SELECT * FROM base where id='{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''Insert INTO base values (?,?,?,?,?,?,?) ''', (message.from_user.id, 1, '', 0, 0, '', 0))
        con.commit()
    await message.answer('Введите: /unfollow (никнейм человека)\nПример: /unfollow elonmusk')





@dp.message_handler(lambda message:  '💳 Купить подписку' == message.text)
async def process_start_command(message: types.Message):
    if cur.execute(f'''SELECT * FROM base where id='{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''Insert INTO base values (?,?,?,?,?,?,?) ''', (message.from_user.id, 1, '', 0, 0, '', 0))
        con.commit()

    I_m2 = InlineKeyboardMarkup()
    I_m2.add(InlineKeyboardButton(f'''Эконом : {str(cur.execute("select econom from payment").fetchall()[0][0])}р/Мес - 1 подписка''',callback_data='oplata1'))
    I_m2.add(InlineKeyboardButton(f'''Стандарт : {str(cur.execute("select standart from payment").fetchall()[0][0])}р/Мес - 3 подписки''', callback_data='oplata2'))
    I_m2.add(InlineKeyboardButton(f'''Премиум : {str(cur.execute("select premium from payment").fetchall()[0][0])}р/Мес - 9 подписок ''', callback_data='oplata3'))
    I_m2.add(InlineKeyboardButton(f'''Платина : {str(cur.execute("select platina from payment").fetchall()[0][0])}р/Мес - 15 подписок ''', callback_data='oplata4'))
    I_m2.add(InlineKeyboardButton('⬅️ Назад', callback_data='nazad'))
    await message.answer('Оплата:',reply_markup=I_m2)

@dp.callback_query_handler(text='nazad')
async def oplata(message : types.CallbackQuery):
    try:
        await bot.delete_message(message.message.chat.id, message_id=message.message.message_id)
        await bot.delete_message(message.message.chat.id, message_id=message.message.message_id - 1)
    except:
        pass

@dp.callback_query_handler(text_contains='oplata')
async def oplata(message : types.CallbackQuery):
    await bot.delete_message(message.message.chat.id,message_id=message.message.message_id)
    await bot.delete_message(message.message.chat.id, message_id=message.message.message_id-1)
    if message.data == 'oplata1':
        pay = cur.execute('''select econom from payment''').fetchall()[0][0]
    elif message.data == 'oplata2':
        pay = cur.execute('''select standart from payment''').fetchall()[0][0]
    elif message.data == 'oplata3':
        pay = cur.execute('''select premium from payment''').fetchall()[0][0]
    elif message.data == 'oplata4':
        pay = cur.execute('''select platina from payment''').fetchall()[0][0]
    uid = ''.join([random.choice(azlf) for x in range(100)])
    cur.execute(f'''UPDATE base set uid = '{uid}' where id = '{message.from_user.id}' ''')
    con.commit()
    s7 = requests.Session()
    headers = {
        'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjJid3ZiYi0wMCIsInVzZXJfaWQiOiI5OTQ3MDkxODQwODQiLCJzZWNyZXQiOiI5YjViNTE2ZTBmZWRhNDc4YTc3YTc2NGRiODFlYmFmMzZiNjZmZWVhNjcwODBiNDMyMGEzYjA1MTA0MmM4N2RmIn19',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    params = {'amount': {'value': pay,
                         'currency': 'RUB',
                         },
              'comment': 'Оплата подписки',
              'expirationDateTime': '2030-04-13T14:30:00+03:00',
              'customer': {},
              'customFields': {},
              }
    params = json.dumps(params)
    p = s7.put(f'https://api.qiwi.com/partner/bill/v1/bills/{uid}', data=params, headers=headers)
    I_m1 = InlineKeyboardMarkup()
    I_m1.add(types.InlineKeyboardButton('Оплатить', url=p.json()['payUrl'], callback_data='Оплатить'))
    I_m1.add(types.InlineKeyboardButton('Проверить оплату', callback_data=f'hamali{str(pay)}'))
    await message.message.answer('Оплатить:', reply_markup=I_m1)


@dp.callback_query_handler(text_contains='hamali')
async def process_start_command(message: types.CallbackQuery):
    uid = cur.execute(f'''Select uid from base where id = '{message.from_user.id}' ''').fetchall()


    if message.data == f'hamali{str(cur.execute("select econom from payment").fetchall()[0][0])}':
        balance = 1
    elif message.data == f'hamali{str(cur.execute("select standart from payment").fetchall()[0][0])}':
        balance = 3
    elif message.data == f'hamali{str(cur.execute("select premium from payment").fetchall()[0][0])}':
        balance = 9
    elif message.data == f'hamali{str(cur.execute("select platina from payment").fetchall()[0][0])}':
        balance = 15


    if uid != []:
        uid = uid[0][0]
        s7 = requests.Session()
        headers = {
            'Authorization': 'Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjJid3ZiYi0wMCIsInVzZXJfaWQiOiI5OTQ3MDkxODQwODQiLCJzZWNyZXQiOiI5YjViNTE2ZTBmZWRhNDc4YTc3YTc2NGRiODFlYmFmMzZiNjZmZWVhNjcwODBiNDMyMGEzYjA1MTA0MmM4N2RmIn19',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        p = s7.get(f'https://api.qiwi.com/partner/bill/v1/bills/{uid}', headers=headers)
        print(p.json()['status']['value'])
        if p.json()['status']['value'] == 'PAID':
            cur_ball = int(cur.execute(f'''select balance from base where id = '{message.from_user.id}' ''').fetchall()[0][0])
            if cur_ball == 0:

                cur.execute(f'''UPDATE base set uid = '' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set days = days + 30 where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set balance = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set count = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
            elif cur_ball == balance:
                cur.execute(f'''UPDATE base set uid = '' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set days = days + 30 where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set balance = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set count = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
            elif cur_ball > balance:
                cur.execute(f'''UPDATE base set uid = '' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set days = days + 30 where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set balance = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set count = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
            elif cur_ball < balance:
                cur.execute(f'''UPDATE base set uid = '' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set days = '30' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set balance = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
                cur.execute(f'''UPDATE base set count = '{balance}' where id = '{message.from_user.id}' ''')
                con.commit()
            await message.message.answer('ОПЛАТА ПРОШЛА УСПЕШНО!!!')
        else:
            await message.message.answer('ОПЛАНА НЕ ПРИШЛА')
    else:
        await message.message.answer('Вы не создали оплату')



@dp.message_handler(lambda message:  '🔰 Аккаунт' == message.text)
async def process_start_command(message: types.Message):
    if cur.execute(f'''SELECT * FROM base where id='{message.from_user.id}' ''').fetchall() == []:
        cur.execute('''Insert INTO base values (?,?,?,?,?,?,?) ''', (message.from_user.id, 1, '', 0, 0, '', 0))
        con.commit()
    ball = cur.execute(f'''Select count from base where id = '{message.from_user.id}' ''').fetchall()[0][0]
    days = cur.execute(f'''Select days from base where id = '{message.from_user.id}' ''').fetchall()[0][0]
    follow = cur.execute(f'''Select follows from base where id = '{message.from_user.id}' ''').fetchall()[0][0]
    ostalos = cur.execute(f'''Select balance from base where id = '{message.from_user.id}' ''').fetchall()[0][0]

    if ball == 0:
        ball = 'Нет(0)'
    elif ball == 1:
        ball = 'Эконом(1)'
    elif ball == 3:
        ball = 'Стандарт(3)'
    elif ball == 9:
        ball = 'Премиум(9)'
    elif ball == 15:
        ball == 'Платина(15)'
    else:
        ball == 'God(?)'
    if days == 0:
        ball = 'Нет(0)'
        ostalos = 0
    await message.answer(f'🔰 Ваш id: {message.from_user.id}'
                         f'\n✅ Подписка: {ball} Осталось: ({ostalos})'
                         f'\n⭕️ Осталось дней: {days}'
                         f'''\nПодписки на:''')
    try:
        for i in str(follow).split(','):
            await message.answer(i)
    except:pass





@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    if str(message.from_user.id) not in str(cur.execute('''SELECT id from base''').fetchall()):
        await message.answer('Сначало введите /start')
    else:
        await message.reply("/follow и никнейм\n/unfollow и никнейм")





@dp.message_handler(commands=['follow'])
async def echo_message(msg: types.Message):
    if str(msg.from_user.id) not in str(cur.execute('''SELECT id from base''').fetchall()):
        await msg.answer('Сначало введите /start')
    else:

        a = msg.text.lower()
        a = a.replace('/follow ', '')
        idd = msg.from_user.id
        driver.get(f'https://mobile.twitter.com/{a}')
        try:
            WebDriverWait(driver, 3).until(Ec.presence_of_element_located(
                (By.XPATH, '''//span[text()='Такой учетной записи нет']''')))
            await msg.answer('Такого никнейма нету!')
        except:



            if a.strip() == '/follow':
                await msg.answer('Введите никнейм через пробел ПРИМЕР: /follow elonmusk')
            else:

                balance = cur.execute(f'''select balance from base where id = '{msg.from_user.id}' ''').fetchall()[0][0]
                if balance == 0:
                    await msg.answer('У вас лимит по подпискам')
                else:

                    if cur.execute(f'''SELECT * FROM names where name='{a}' ''').fetchall() == [] and a not in str(cur.execute(f'''SELECT follows FROM base where id='{idd}' ''').fetchall()) :
                        cur.execute(f'''UPDATE base SET follows =follows || '{a},' where id ='{idd}' ''')
                        con.commit()
                        cur.execute('''INSERT into names  values (?,?,?) ''', (f'{a}', 1,''))
                        con.commit()
                        cur.execute(f'''update base set balance = balance - 1 where id = '{msg.from_user.id}' ''')
                        con.commit()
                        await bot.send_message(msg.from_user.id, f'вы подписались на {a}')
                    elif a not in str(cur.execute(f'''SELECT follows FROM base where id='{idd}' ''').fetchall()):
                        cur.execute(f'''UPDATE base SET follows =follows || '{a},' where id ='{idd}' ''')
                        con.commit()
                        cur.execute(f'''UPDATE names  set count = count + 1 where name='{a}' ''')
                        con.commit()
                        cur.execute(f'''update base set balance = balance - 1 where id = '{msg.from_user.id}' ''')
                        con.commit()
                        await bot.send_message(msg.from_user.id, f'вы подписались на {a}')
                    else:
                        await bot.send_message(msg.from_user.id, f'вы и так подписанны на2 {a}')



@dp.message_handler(commands=['unfollow'])
async def echo_message(msg: types.Message):
    if str(msg.from_user.id) not in str(cur.execute('''SELECT id from base''').fetchall()):
        await msg.answer('Сначало введите /start')
    else:
        idd = msg.from_user.id
        a = msg.text.lower()
        a = a.replace('/unfollow ', '')
        if cur.execute(f'''SELECT * FROM names where name='{a}' ''').fetchall() == [] or a not in str(cur.execute(f'''SELECT follows FROM base where id='{idd}' ''').fetchall()[0][0]) :
            await bot.send_message(msg.from_user.id, f'Вы и так не подписанны на {a}')
        elif cur.execute(f'''SELECT count FROM names where name='{a}' ''').fetchall()[0][0] == 1 and a in str(cur.execute(f'''SELECT follows FROM base where id='{idd}' ''').fetchall()):
            qwer = str(cur.execute(f'''Select follows from base where id ='{idd}' ''').fetchall()[0][0]).replace(f'{a},','')
            cur.execute(f'''update base set follows='{qwer}',balance = balance + 1 ''')
            con.commit()
            cur.execute(f'''DELETE from names where name='{a}' ''')
            con.commit()

            await bot.send_message(msg.from_user.id, f'вы отписались от {a}')
        else:
            if a in str(cur.execute(f'''SELECT follows FROM base where id='{idd}' ''').fetchall()):
                qwer = str(cur.execute(f'''Select follows from base where id ='{idd}' ''').fetchall()[0][0]).replace(
                    f'{a},', '')
                cur.execute(f'''update base set follows='{qwer}',balance = balance + 1 ''')
                con.commit()
                cur.execute(f'''UPDATE names set count = count - 1 where name='{a}' ''')
                con.commit()
                await bot.send_message(msg.from_user.id, f'вы отписались от {a}')




async def periodic(sleep_for):

    while True:


        for name in cur.execute('''SELECT name from names''').fetchall():
            name = name[0]
            driver.get(f'https://mobile.twitter.com/{name}')
            try:
                WebDriverWait(driver, 60).until(Ec.presence_of_element_located(
                    (By.XPATH, '''//main//div[@class='css-1dbjc4n']//section//div[@class='css-1dbjc4n']//article''')))
                a = driver.find_elements_by_xpath(
                    '''//main//div[@class='css-1dbjc4n']//section//div[@class='css-1dbjc4n']//article''')
                pinned = driver.find_elements_by_xpath('''//div[@class='css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l']''')
                number = 0
                for i in pinned:
                    b = i.find_elements_by_xpath('''div/div/div//span''')
                    for j in b:
                        if j.text == 'Закрепленный твит' or j.text == 'Pinned Tweet':
                            number = 1
                            break
                    break
                a[number] = a[number]
                texts = ' '.join((a[number].find_element_by_xpath(
                    '''div//div[@class='css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']''').text).split())
                photos = [x.get_attribute('src') for x in a[number].find_elements_by_xpath(
                    '''div//div[@class='r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu']//img[@alt='Изображение']''')]
                result = trans.translate(texts)
                if cur.execute(f'''SELECT twit from names where name = '{name}' ''').fetchall()[0][0] != result:

                    for sends in cur.execute(f'''SELECT id from base where follows LIKE '%{name}%' AND subscribe = '1' and days != 0  ''').fetchall():
                        if cur.execute(f'''select days from base where id ='{sends}' ''').fetchall()[0][0] == 0:
                            if cur.execute(f'''SELECT count FROM names where name='{a}' ''').fetchall()[0][0] == 1 and a in str(cur.execute(f'''SELECT follows FROM base where id='{idd}' ''').fetchall()):
                                qwer = str(cur.execute(f'''Select follows from base where id ='{sends}' ''').fetchall()[0][0]).replace(f'{a},', '')
                                cur.execute(f'''update base set follows='{qwer}',balance = '0',count = '0' ''')
                                con.commit()
                                cur.execute(f'''DELETE from names where name='{a}' ''')
                                con.commit()

                            else:
                                if a in str(cur.execute(f'''SELECT follows FROM base where id='{sends}' ''').fetchall()):
                                    qwer = str(cur.execute(f'''Select follows from base where id ='{sends}' ''').fetchall()[0][0]).replace(f'{a},', '')
                                    cur.execute(f'''update base set follows='{qwer}',balance = '0',count = '0' ''')
                                    con.commit()
                                    cur.execute(f'''UPDATE names set count = count - 1 where name='{a}' ''')
                                    con.commit()
                        else:
                            await bot.send_message(int(sends[0]),'@'+name+'\n'+result)
                            for pot in photos:
                                await bot.send_photo(int(sends[0]),pot)
                cur.execute(f'''UPDATE names SET twit = '{result}' where name = '{name}' ''')
                con.commit()
                await asyncio.sleep(sleep_for)
            except:pass
        await asyncio.sleep(60)


######################################################################################################################################3


@dp.message_handler(lambda message:  'all' in message.text)
async def echo_message(msg: types.Message):
    if msg.from_user.id ==  484026432 or msg.from_user.id ==  1784451390:
        a = cur.execute('''SELECT id,days,balance from base''').fetchall()
        b = '\n'.join([str(x[0])+'|| Дни: '+str(x[1])+"|| Количество возможных подписок: "+str(x[2]) for x in a])
        await msg.answer(b)
        await msg.answer(f'Количество пользователей: {len(a)}')

@dp.message_handler(lambda message:  'add' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id ==  484026432 or message.from_user.id ==  1784451390:
        id,days = (message.text).split(' ')[0],(message.text).split(' ')[2]
        cur.execute(f'''UPDATE base set days = days + {days}  where id = '{int(id)}' ''')
        con.commit()
        await message.answer('Получилось')

@dp.message_handler(lambda message:  'minus' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id ==  484026432 or message.from_user.id ==  1784451390:
        id,days = (message.text).split(' ')[0],(message.text).split(' ')[2]
        if int(cur.execute(f'''select days from base where id = '{int(id)}' ''').fetchall()[0][0]) < int(days):
            cur.execute(f'''UPDATE base set days = '0'  where id = '{int(id)}' ''')
            con.commit()
        else:
            cur.execute(f'''UPDATE base set days = days - {days} where id = '{int(id)}' ''')
            con.commit()
        await message.answer('Получилось')

@dp.message_handler(lambda message:  'info' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id ==  484026432 or message.from_user.id ==  1784451390:
        id = message.text.split(' ')[0]
        a = cur.execute(f'''Select * from base where id = '{id}' ''').fetchall()
        if a != []:
            await message.answer(f'{id}\nПодписки: {a[0][2]}\nКоличество доступных подписок: {a[0][3]}\nДни: {a[0][4]}\nId чека: {a[0][5]}')

@dp.message_handler(lambda message:  'set econom' in message.text.lower())
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        money = message.text.split(' ')[2]
        cur.execute(f'''update payment set econom = '{money}' ''')
        con.commit()
        await message.answer(f'Успешно изменили цену на {money}')
@dp.message_handler(lambda message:  'set standart' in message.text.lower())
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        money = message.text.split(' ')[2]
        cur.execute(f'''update payment set standart = '{money}' ''')
        con.commit()
        await message.answer(f'Успешно изменили цену на {money}')
@dp.message_handler(lambda message:  'set premium' in message.text.lower())
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        money = message.text.split(' ')[2]
        cur.execute(f'''update payment set premium = '{money}' ''')
        con.commit()
        await message.answer(f'Успешно изменили цену на {money}')
@dp.message_handler(lambda message:  'set platina' in message.text.lower())
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        money = message.text.split(' ')[2]
        cur.execute(f'''update payment set platina = '{money}' ''')
        con.commit()
        await message.answer(f'Успешно изменили цену на {money}')



@dp.message_handler(lambda message:  'admin' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        maka = ReplyKeyboardMarkup(resize_keyboard=True)
        maka.add(KeyboardButton('all'))
        maka.row(KeyboardButton('payment'),KeyboardButton('Поменять цену'))
        maka.add(KeyboardButton('Добавить или убрать Дни'),KeyboardButton('Добавить кол-во подписки'))
        maka.add(KeyboardButton('Узнать о пользователе'))
        maka.add(KeyboardButton('Промокоды'))
        maka.add(KeyboardButton('/start'))
        await message.answer('Добро пожаловать мой повелитель!',reply_markup=maka)

@dp.message_handler(lambda message: 'Узнать о пользователе' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        await message.answer(f'Варианты: info\nПример: 14654446546 info\nВыдает всю информацию о пользователе')



@dp.message_handler(lambda message: 'Поменять цену' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        await message.answer(f'Варианты: econom,standart,premium,platina\nПример: set econom 101')

@dp.message_handler(lambda message: 'Узнать о пользователе' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        await message.answer(f'Варианты: info\nПример: 14654446546 info\nВыдает всю информацию о пользователе')

@dp.message_handler(lambda message: 'Промокоды' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        qw = ReplyKeyboardMarkup(resize_keyboard=True)
        qw.add(KeyboardButton('Создать Промокод'))
        qw.add(KeyboardButton('Не использованные промокоды'))
        qw.add(KeyboardButton('Удалить все промокоды'))
        qw.add(KeyboardButton('admin'))
        await message.answer(f'Мир промокодов',reply_markup=qw)


@dp.message_handler(lambda message: 'Удалить все промокоды' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        cur.execute('''DELETE from promo''')
        con.commit()
        await message.answer('Успешно удалено')

@dp.message_handler(lambda message: 'Создать Промокод' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        await message.answer('Инструкция: create [количество промокодов] [Количество дней] [количество подписчиков]\nПример: create 1 30 3')


@dp.message_handler(lambda message: 'Не использованные промокоды' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        for i in cur.execute('''Select * from promo''').fetchall():
            await message.answer(f'{i[0]} {i[1]} {i[2]}')

@dp.message_handler(lambda message: 'create' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        a = message.text.split(' ')
        if len(a) != 4:
            await message.answer('Не правильно ввели команду')
        else:
            for i in range(int(a[1])):
                b = ''.join([random.choice(azlf) for x in range(7)])
                cur.execute('''insert into promo values(?,?,?)''',(b,int(a[2]),int(a[3])))
                con.commit()
                await message.answer(b)

@dp.message_handler(lambda message: 'Добавить кол-во подписки' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        await message.answer(f'Варианты: up,down\nПример: 4548478454 up 3\nЧто означает такому то id добавили 3 подписки')


@dp.message_handler(lambda message: 'Добавить или убрать Дни' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        await message.answer(f'Варианты, add,minus\nПример: 1849745613 add 30\nЧто означает такому то id добавили 30 дней')

@dp.message_handler(lambda message:  'payment' in message.text)
async def process_help_command(message: types.Message):
    if message.from_user.id == 484026432 or message.from_user.id == 1784451390:
        await message.answer(f'''Econom: {cur.execute("select econom from payment").fetchall()[0][0]}''')
        await message.answer(f'''Standart: {cur.execute("select standart from payment").fetchall()[0][0]}''')
        await message.answer(f'''Premium: {cur.execute("select premium from payment").fetchall()[0][0]}''')
        await message.answer(f'''Platina: {cur.execute("select platina from payment").fetchall()[0][0]}''')



async def timer():
    while True:
        for i in cur.execute('''SELECT days,id from base''').fetchall():
            id = i[1]
            days = i[0]
            if days > 1:
                cur.execute(f'''update base set days = days - 1 where id ='{id}' ''')
                con.commit()
            elif days == 1:
                cur.execute(f'''update base set days = days - 1 where id ='{id}' ''')
                con.commit()
                await bot.send_message(id,'Ваша подписка закончилась')
        await asyncio.sleep(60*60*24)



if __name__ == '__main__':
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("window-size=1920x1080")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome()
    # trans = GoogleTranslator(source='english', target='ru')
    # loop = asyncio.get_event_loop()
    # loop.create_task(periodic(5))
    # loop2 = asyncio.get_event_loop()
    # loop2.create_task(timer())
    executor.start_polling(dp, skip_updates=True)

