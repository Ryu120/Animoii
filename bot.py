from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram import Client, filters
import tracemoepy
from requests import get
import time , datetime
import os
import re


API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)


bot = Client(
    "Kawaii",
    api_id = API_ID, 
    api_hash = API_HASH, 
    bot_token = BOT_TOKEN)

def call_back_in_filter(data):
    return filters.create(
        lambda flt, _, query: flt.data in query.data,
        data=data
    )

def latest():

    url = 'https://subsplease.org/api/?f=schedule&h=true&tz=Japan'
    res = get(url).json()

    k = None 
    for x in res['schedule']:
        title = x['title']
        time = x['time']
        aired = bool(x['aired'])
        title = f"**[{title}](https://subsplease.org/shows/{x['page']})**" if not aired else f"**~~[{title}](https://subsplease.org/shows/{x['page']})~~**"
        data = f"{title} - {time}"

        if k:
            k = f"{k}\n{data}"

        else:
            k = data


    return k



@bot.on_message(filters.command('latest'))
def lates(_,message):
    mm = latest()
    message.reply_text(f"Today's Schedule:\nTZ: Japan\n{mm}" , reply_markup=InlineKeyboardMarkup(
    [    
        [InlineKeyboardButton("Refresh" , callback_data="animoii")]

    ]
        
    ))


@bot.on_callback_query(call_back_in_filter("animoii"))
def callbackk(_,query):

    if query.data == "animoii":
        mm = latest()
        time_ = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M")


        try:
            query.message.edit(f"Today\'s Schedule:\nTZ: Japan\n{mm}", reply_markup=InlineKeyboardMarkup(
        [    
            [InlineKeyboardButton("Refresh" , callback_data="animoii")]

        ]
            
        ))
            query.answer("Refreshed!")


        except:
            query.answer("Refreshed!")

tracemoe = tracemoepy.tracemoe.TraceMoe()

@bot.on_message(filters.command('whatanime'))
def whatanime(_,message):
  reply = message.reply_to_message
  if reply and reply.media:
    path = reply.download()
    info = tracemoe.search(path, upload_file=True)
    data = f"Match: {info.result[0].anilist.title.romaji}\nSimilarity: {info.result[0].similarity*100}"
    info.result[0].save(f"{reply.from_user.id}.mp4", mute = False)
    reply.reply_document(f"{reply.from_user.id}.mp4" , caption=data)
    os.remove(f"{reply.from_user.id}.mp4")     
            



if __name__ == "__main__":
    bot.run()
