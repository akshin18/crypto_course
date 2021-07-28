import re
import asyncio

from bs4 import BeautifulSoup as bs
from telegraph import Telegraph
import requests
import json
import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



TOKEN = '1890561220:AAE0_UyC7VsyoqjcUbVeGoigbdMsnyatu3M'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
numbers = '1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟'.split(' ')
con = sqlite3.connect('aqw.db')
cur = con.cursor()


'''
http://static.feed.rbc.ru/rbc/logical/footer/news.rss

https://forklog.com/news/feed/

https://letknow.news/xml/rss.html

https://bits.media/rss2/

https://cryptocurrency.tech/feed

https://news.bitcointalk.com/feed/

https://coinspot.io/feed

https://ru.investing.com/rss/302.rss

https://beincrypto.ru/news/feed/
'''

async def forklog(con,cur):

    try:
        r = requests.get('https://forklog.com/news/feed/',timeout=30)
        soup = bs(r.text,'lxml')

        item = soup.find('item')


        find = item.find('description')
        title = item.find('title').text
        # print(find)
        if cur.execute('''SELECT link from links where name='forklog' ''').fetchall()[0][0] != str(title):
            dava = []
            one = 0
            for stir in find:
                if '<img' in str(stir):
                    qwe = re.findall('''<img(.*?)\/>''',str(stir))
                    for i in qwe:
                        dava.append('<img'+i+'/>')
                elif '<p>' in str(stir):
                    qwe = re.findall('''<p>(.*?)<\/p>''',str(stir))
                    for i in qwe:

                        try:
                            i = str(i).replace('<a','<b')
                            i = i.replace('a>','b>')
                        except:continue
                        if 'Подписывайтесь на ' not in i:
                            if one == 0:
                                dava.append('<p>🗣 '+i+'</p>')
                                one += 1
                            else:
                                dava.append('<p>' + i.replace('ForkLog','Крипто ฿ести') + '</p>')
                elif '<li>' in str(stir):
                    qwe = re.findall('''<li>(.*?)<\/li>''', str(stir))
                    for i in qwe:
                        dava.append('<li>' + i + '</li>')
            if len(dava) < 3:
                return

            dava.append('<p>🔝 <a href="#_tl_editor">В начало статьи</a> 📲 <a href="https://t.me/kripto_vesti" target="_blank">Подписаться на канал</a></p>')
        #################################################################################################333

            telegraph = Telegraph(access_token=cur.execute('''select access from token''').fetchall()[0][0])
            # telegraph.create_account(short_name='dinazavr')
            # print(telegraph.get_access_token())
            # print(telegraph.get_account_info())
            response = telegraph.create_page(
                f'⚡️{title}',
                html_content=''.join(dava),
                author_url='https://t.me/kripto_vesti',
                author_name='📰 Крипто ฿ести'
            )
            cur.execute(f'''UPDATE links set  link='{title}' where name='forklog' ''')
            con.commit()
            await bot.send_message(-1001568421085,
                                   f'<a href="https://telegra.ph/{response["path"]}">от🐺Волка:</a>',
                                   parse_mode='HTML')

            print('https://telegra.ph/{}'.format(response['path']))
    except Exception as e:
        print(e,'forklog')

async def coinspot(con,cur):
    try:
        r = requests.get('https://coinspot.io/feed/',timeout=30)
        # r = open('123.html')
        soup = bs(r.text, 'lxml')

        item = soup.find('item')
        find = item.find('content:encoded')
        title = item.find('title').text
        if cur.execute('''SELECT link from links where name='coinspot' ''').fetchall()[0][0] != str(title):
            dava = []
            dava.append('🗣 '+find.text.split('\n')[0])
            one = 0
            for stir in find:
                # print(stir)
                if '<img' in str(stir):
                    qwe = re.findall('''<img(.*?)\/>''', str(stir))
                    for i in qwe:
                        dava.append('<img' + i + '/>')
                elif '<p>' in str(stir):

                    qwe = re.findall('''<p>(.*?)<\/p>''', str(stir))
                    for i in qwe:
                        try:
                            i = str(i).replace('<a', '<b')
                            i = i.replace('a>', 'b>')
                        except:
                            continue
                        if 'Подписывайтесь на новости ForkLog' not in i:

                            dava.append('<p>' + i + '</p>')
                elif '<li>' in str(stir):
                    qwe = re.findall('''<li>(.*?)<\/li>''', str(stir))
                    for i in qwe:
                        dava.append('<li>' + i + '</li>')
            dava.append(
                '<p>🔝 <a href="#_tl_editor">В начало статьи</a> 📲 <a href="https://t.me/kripto_vesti" target="_blank">Подписаться на канал</a></p>')
            #################################################################################################333
            telegraph = Telegraph(access_token=cur.execute('''select access from token''').fetchall()[0][0])

            response = telegraph.create_page(
                f'⚡️{title}',
                html_content=''.join(dava),
                author_url='https://t.me/kripto_vesti',
                author_name='📰 Крипто ฿ести'
            )
            cur.execute(f'''UPDATE links set  link='{title}' where name='coinspot' ''')
            con.commit()
            await bot.send_message(-1001568421085,
                                   f'<a href="https://telegra.ph/{response["path"]}">от🐺Волка:</a>',
                                   parse_mode='HTML')
            # print('https://telegra.ph/{}'.format(response['path']))
    except Exception as e:print(e,'coinspot')

async def beincrypto(con,cur):
    try:

        r = requests.get('https://beincrypto.ru/news/feed/',timeout=30)

        # r = open('123.html')
        soup = bs(r.text, 'lxml')
        item = soup.find('item')
        find = item.find('content:encoded')
        title = item.find('title').text
        if cur.execute('''SELECT link from links where name='beincrypto' ''').fetchall()[0][0] != str(title):
            dava = []
            dava.append('🗣 '+find.text.split('\n')[0])
            one = 0
            for stir in find:
                # print(stir)
                if '<img' in str(stir):
                    qwe = re.findall('''<img(.*?)\/>''', str(stir))
                    for i in qwe:
                        dava.append('<img' + i + '/>')
                elif '<p>' in str(stir):

                    qwe = re.findall('''<p>(.*?)<\/p>''', str(stir))
                    for i in qwe:
                        try:
                            i = str(i).replace('<a', '<b')
                            i = i.replace('a>', 'b>')
                        except:
                            continue
                        if 'Подписывайтесь на новости ForkLog' not in i and 'Читайте также:' not in i :

                            dava.append('<p>' + (i.replace('span','b')).replace('BeInCrypto','Крипто ฿ести').replace('Также на ForkLog:','') + '</p>')
                elif '<li>' in str(stir):
                    qwe = re.findall('''<li>(.*?)<\/li>''', str(stir))
                    for i in qwe:
                        dava.append('<li>' + i + '</li>')
            dava.append(
                '<p>🔝 <a href="#_tl_editor">В начало статьи</a> 📲 <a href="https://t.me/kripto_vesti" target="_blank">Подписаться на канал</a></p>')
            #################################################################################################333
            telegraph = Telegraph(access_token=cur.execute('''select access from token''').fetchall()[0][0])
            # print(dava)
            response = telegraph.create_page(
                f'⚡️{title}',
                html_content=''.join(dava),
                author_url='https://t.me/kripto_vesti',
                author_name='📰 Крипто ฿ести'
            )
            cur.execute(f'''UPDATE links set  link='{title}' where name='beincrypto' ''')
            con.commit()
            await bot.send_message(-1001568421085,
                                   f'<a href="https://telegra.ph/{response["path"]}">от🐺Волка:</a>',
                                   parse_mode='HTML')
    except Exception as e:print(e,'beincrypto')
async def main():
    await asyncio.sleep(3)
    con = sqlite3.connect('aqw.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS links (
    name text,
    link text
    ); ''')



    while True:
        await forklog(con,cur)
        await coinspot(con,cur)
        await beincrypto(con,cur)
        await asyncio.sleep(300)


@dp.message_handler()
async def ewfrew(message:types.Message):
    if message.from_user.id == 1786797801 and message.text == 're':

        c = Telegraph(access_token=cur.execute('''select access from token''').fetchall()[0][0])
        pom = c.revoke_access_token()
        cur.execute(f'''UPDATE token set access = '{pom['access_token']}' ''')
        con.commit()

        await message.answer(pom)





@dp.channel_post_handler()
async def ewfrew(message:types.Message):
    if message.text == '/crypto':

        try:
            try:
                await message.delete()
            except:pass
            cuta = InlineKeyboardMarkup()
            url = 'https://api.coincap.io/v2/assets'
            r = requests.get(url)
            data = json.loads(r.text)

            categories = [[numbers[int(i['rank']) - 1] + ' ' + i["symbol"] if len(
                numbers[int(i['rank']) - 1] + ' ' + i["symbol"]) == 8 else numbers[int(i['rank']) - 1] + '    ' + i[
                "symbol"], '💲' + i['priceUsd'][:5] if int(float(i['priceUsd'][:7])) < 2 else (
                '💲' + i['priceUsd'][:7] if int(float(i['priceUsd'][:7])) < 999 else '💲' + (str(
                    int(float(i['priceUsd'][:7])))[::-1][:3] + ',' + str(int(float(i['priceUsd'][:7])))[::-1][3:])[
                                                                                            ::-1] + '.' +
                                                                                     i['priceUsd'][:7][::-1].split('.')[
                                                                                         0][::-1]),
                           '🔴️ ' + str(i['changePercent24Hr']).split('.')[0]+'.'+str(i['changePercent24Hr']).split('.')[1][:2] + ' %' if '-' in str(
                               i['changePercent24Hr'][:5]) else '🟢+' + str(
                               int(float(i['changePercent24Hr'][:5]))) + '.' + i['changePercent24Hr'][:5].split('.')[1][
                                                                               :2] + ' %'] for i in data['data'][:10]]
            # for i in categories:
            #     print(i[0], len(i[0]))
            for i in categories:
                cuta.add(InlineKeyboardButton(i[0], callback_data='e'), InlineKeyboardButton(i[1], callback_data='e'),
                         InlineKeyboardButton(i[2], callback_data='e'))

            await bot.send_photo(message.chat.id, open('header6.jpg', 'rb').read(), reply_markup=cuta)

        except Exception as e:
            print(e)


async def course():
    while True:
        try:
            cuta = InlineKeyboardMarkup()
            url = 'https://api.coincap.io/v2/assets'
            r = requests.get(url)
            data = json.loads(r.text)

            categories = [[numbers[int(i['rank']) - 1] + ' ' + i["symbol"] if len( numbers[int(i['rank']) - 1] + ' ' + i["symbol"]) == 8 else numbers[int(i['rank']) - 1] + '    ' + i["symbol"],'💲' + i['priceUsd'][:5] if int(float(i['priceUsd'][:7])) < 2 else ( '💲' + i['priceUsd'][:7] if int(float(i['priceUsd'][:7])) < 999 else '💲' + (str( int(float(i['priceUsd'][:7])))[::-1][:3] + ',' + str(int(float(i['priceUsd'][:7])))[::-1][ 3:])[::-1] ),'🔴️ ' + str(i['changePercent24Hr']).split('.')[0]+'.'+str(i['changePercent24Hr']).split('.')[1][:2] + ' %' if '-' in str(i['changePercent24Hr'][:5]) else '🟢+' + str(int(float(i['changePercent24Hr'][:5]))) + '.' +i['changePercent24Hr'][:5].split('.')[1][:2] + ' %'] for i in data['data'][:10]]

            # for i in categories:
            #     print(i[0], len(i[0]))
            for i in categories:
                cuta.add(InlineKeyboardButton(i[0], callback_data='e'), InlineKeyboardButton(i[1], callback_data='e'),
                         InlineKeyboardButton(i[2], callback_data='e'))

            await bot.send_photo(-1001568421085, open('header6.jpg', 'rb').read(), reply_markup=cuta)
            await asyncio.sleep(14400)
        except Exception as e:print(e)


if __name__ == '__main__':
    # loop2 = asyncio.get_event_loop()
    # loop2.create_task(course())
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)


