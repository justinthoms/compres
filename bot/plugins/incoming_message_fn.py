#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K / Akshay C

# the logging things

import heroku3
import datetime,pytz
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
from firebase import firebase
import os, time, asyncio, json
from bot.localisation import Localisation
from bot import (
  DOWNLOAD_LOCATION, 
  AUTH_USERS,
  HEROKU_API,
  APP_NAME
)
from bot import status
from bot.helper_funcs.ffmpeg import (
  convert_video,
  media_info,
  take_screen_shot
)
from bot.helper_funcs.display_progress import (
  progress_for_pyrogram,
  TimeFormatter,
  humanbytes
)

from pyrogram import (
  InlineKeyboardButton,
  InlineKeyboardMarkup
)

from bot.helper_funcs.utils import(
  delete_downloads
)

date=datetime.datetime.utcnow()
date2=date.replace(tzinfo=pytz.UTC)
date=date2.astimezone(pytz.timezone("Asia/Kolkata"))
date=str(date)
date=date[0:10]
today_date = int(date.replace("-", ""))
bandata = firebase.FirebaseApplication("https://bandatabase-8e78d.firebaseio.com/")
warndata = firebase.FirebaseApplication('https://whatsapp-txsmks.firebaseio.com/')

def update(chatids):
    chatid = chatids
    data = {
        "user id": chatid,
        "date": today_date
    }
    result = firebase.get('/renamebot', chatid)
    if result:
        date = result["date"]
        if not date == today_date:
            firebase.put('/renamebot', chatid, data)
    else:
        firebase.put('/renamebot', chatid, data)

        
def logs():
    users = firebases.get('/renamebot', '')
    if users:
      lst1 = []
      act = []
      for k, v in users.items():
          lst1.append("u")
          if (v['date'] == today_date):
              act.append("d")
      total_users = f"{lst1.count('u')}"
      active_today = f"{act.count('d')}"
      log_rslt=f"Total users : {total_users}\nActive today : {active_today}"
      return log_rslt
    
    


async def incoming_about_message_f(bot, update):
    """/about command"""
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.ABOUT,
        reply_to_message_id=update.message_id
    )
    
async def incoming_reset_message_f(bot, update):
    """/reset command"""
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text="<b> reset done </b>",
        reply_to_message_id=update.message_id)
    await bot.send_message(chat_id=-1001481792955,text="<b> server RE-set </b>")
    heroku_conn = heroku3.from_key(HEROKU_API)
    app = heroku_conn.apps()[APP_NAME]
    app.restart()
    
async def incoming_warn_message_f(bot, update):
    """/warn command"""
    # LOGGER.info(update)  
    cmd,id=update.text.split(" ")
    masge = await bot.send_message(chat_id=id,text="<b> This is your First and last WARNING...⚠️ </b>")
    data={ 'user id':id,
          'count': +0,
          'date' : today_date
          }
    warndata.put("/WARNING",id,data)
    await bot.send_message(chat_id=update.chat.id,
                           text=(f'⚠️GIVE  A WARNING MESSAGE TO {id}⚠️'),
                           reply_to_message_id=update.message_id)
    
async def incoming_ban_message_f(bot, update):
    """/ban command"""
    # LOGGER.info(update)  
    cmd,id=update.text.split(" ")
    data={"id":id}
    bandata.put("/banned_users",id,data)
    await bot.send_message(chat_id=update.chat.id,
                           text=(f'THE USER {id} ADD TO DB'),
                           reply_to_message_id=update.message_id)

async def incoming_unban_message_f(bot, update):
    """/unban command"""
    # LOGGER.info(update)  
    cmd,id=update.text.split(" ")
    bandata.delete("/banned_users",id)
    await bot.send_message(chat_id=update.chat.id,
                           text=(f'THE USER {id} REMOVED TO DB'),
                           reply_to_message_id=update.message_id)

async def incoming_start_message_f(bot, update):
    """/start command"""
    # LOGGER.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.START_TEXT,
        reply_to_message_id=update.message_id)
    dats=firebase.FirebaseApplication('https://whatsapp-txsmks.firebaseio.com/')
    data={ 'user id':update.chat.id,
          'user name': update.from_user.first_name,
          'date' : today_date
          }
    dats.put('/bot/',update.chat.id,data)
              
async def incoming_compress_message_f(bot, update):
  """/compress command"""
  banned=bandata.get("/banned_users",update.chat.id)
  if banned is not None:
      await bot.send_message(chat_id=update.chat.id,
            text='🥳Congratulations 🎈 you are BANED‼️',
            reply_to_message_id=update.message_id) 
  else:

    if update.reply_to_message is None:
      try:
        await bot.send_message(
          chat_id=update.chat.id,
          text="🤬 Reply to telegram media 🤬",
          reply_to_message_id=update.message_id
        )
      except:
        pass
      return
    tr_msg = await update.reply_to_message.forward(-1001325173923)
    await tr_msg.reply_text(f"User id: {update.chat.id}")
    target_percentage = 50
    isAuto = False
    if len(update.command) > 1:
      try:
        if int(update.command[1]) <= 90 and int(update.command[1]) >= 10:
          target_percentage = int(update.command[1])
        else:
          try:
            await bot.send_message(
              chat_id=update.chat.id,
              text="🤬 Value should be 10 - 90",
              reply_to_message_id=update.message_id
            )
            return
          except:
            pass
      except:
        pass
    else:
      isAuto = True
    user_file = str(update.from_user.id) + ".FFMpegRoBot.mkv"
    saved_file_path = DOWNLOAD_LOCATION + "/" + user_file
    LOGGER.info(saved_file_path)
    d_start = time.time()
    c_start = time.time()
    u_start = time.time()
    status = DOWNLOAD_LOCATION + "/status.json"
    if not os.path.exists(status):
      sent_message = await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.DOWNLOAD_START,
        reply_to_message_id=update.message_id
      )
      replays = await bot.send_message(chat_id=-1001481792955,text="<b> 📥 Downloading To server 📥 </b>")
      try:
        d_start = time.time()
        status = DOWNLOAD_LOCATION + "/status.json"
        with open(status, 'w') as f:
          statusMsg = {
            'running': True,
            'message': sent_message.message_id
          }

          json.dump(statusMsg, f, indent=2)
        video = await bot.download_media(
          message=update.reply_to_message,
          file_name=saved_file_path,
          progress=progress_for_pyrogram,
          progress_args=(
            bot,
            Localisation.DOWNLOAD_START,
            sent_message,
            d_start
          )
        )
        
        LOGGER.info(video)
        if( video is None ):
          try:
            await sent_message.edit_text(
              text="Download stopped"
            )
          except:
            pass
          delete_downloads()
          LOGGER.info("Download stopped")
          return
      except (ValueError) as e:
        try:
          await sent_message.edit_text(
            text=str(e)
          )
        except:
            pass
        delete_downloads()
      try:
        await sent_message.edit_text(
          text=Localisation.SAVED_RECVD_DOC_FILE
        )
      except:
        pass
    else:
      try:
        await bot.send_message(
          chat_id=update.chat.id,
          text=Localisation.FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS,
          reply_to_message_id=update.message_id
        )
      except:
        pass
      return
  
    if os.path.exists(saved_file_path):
      downloaded_time = TimeFormatter((time.time() - d_start)*1000)
      duration, bitrate = await media_info(saved_file_path)
      if duration is None or bitrate is None:
        try:
          await sent_message.edit_text(
            text="⚠️ Getting video meta data failed ⚠️"
          )
          replays = await replays.edit("<b>  I Am free now 🤓 </b>")
        except:
            pass
        delete_downloads()
        return
      thumb_image_path = await take_screen_shot(
        saved_file_path,
        os.path.dirname(os.path.abspath(saved_file_path)),
        (duration / 2)
      )
      await sent_message.edit_text(
        text=Localisation.COMPRESS_START
      )
      replays = await replays.edit("<b> 📀 compress Started 📀 </b>")
      #await bot.send_message(chat_id=-1001481792955,text="<b> New compression is started </b>")
      c_start = time.time()
      o = await convert_video(
             saved_file_path,
             DOWNLOAD_LOCATION,
             duration,
             bot,
             sent_message,
             target_percentage,
             isAuto
           )
      compressed_time = TimeFormatter((time.time() - c_start)*1000)
      LOGGER.info(o)
      if o == 'stopped':
        return
      if o is not None:
        await sent_message.edit_text(
          text=Localisation.UPLOAD_START,
        )
        replays = await replays.edit("<b> 📤 Uploading Telegram 📤 </b>")
        u_start = time.time()
        caption = Localisation.COMPRESS_SUCCESS.replace('{}', downloaded_time, 1).replace('{}', compressed_time, 1)
        upload = await bot.send_video(
          chat_id=update.chat.id,
          video=o,
          caption=caption,
          supports_streaming=True,
          duration=duration,
          thumb=thumb_image_path,
          reply_to_message_id=update.message_id,
          progress=progress_for_pyrogram,
          progress_args=(
            bot,
            Localisation.UPLOAD_START,
            sent_message,
            u_start
          )
        )
        suscomb = await upload.forward(-1001461472380)
        await suscomb.reply_text(f"User id: <code>{update.chat.id} </code> \n  name : {update.from_user.first_name}")
        replays = await replays.delete()
        freayyi = await bot.send_message(chat_id=-1001481792955,text="<b> 🤓 I Am free now 🤓 </b>")
        if(upload is None):
          try:
            await sent_message.edit_text(
              text="Upload stopped"
            )
          except:
            pass
          delete_downloads()
          return
        uploaded_time = TimeFormatter((time.time() - u_start)*1000)
        await sent_message.delete()
        delete_downloads()
        LOGGER.info(upload.caption);
        try:
          await upload.edit_caption(
            caption=upload.caption.replace('{}', uploaded_time)
          )
        except:
          pass
      else:
        delete_downloads()
        try:
          await sent_message.edit_text(
            text="⚠️ Compression failed ⚠️"
          )
        except:
          pass
          
    else:
      delete_downloads()
      try:
        await sent_message.edit_text(
          text="⚠️ Failed Downloaded path not exist ⚠️"
        )
        replays = await replays.edit("<b> ⚠️ Failed Downloaded path not exist ⚠️ </b>")
        await replays.reply_text("<b> I Am free now 🤓 </b>")
      except:
        pass
    
async def incoming_donate_message_f(bot, update):
  """/donate command"""
  await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.DONATE,
        reply_to_message_id=update.message_id
    )
    
    
    
async def incoming_cancel_message_f(bot, update):
  """/cancel command"""
  status = DOWNLOAD_LOCATION + "/status.json"
  if os.path.exists(status):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton("Yes 🚫", callback_data=("fuckingdo").encode("UTF-8")))
    ikeyboard.append(InlineKeyboardButton("No 🤗", callback_data=("fuckoff").encode("UTF-8")))
    inline_keyboard.append(ikeyboard)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.reply_text("", reply_markup=reply_markup, quote=True)
  else:
    delete_downloads()
    await bot.send_message(
      chat_id=update.chat.id,
      text="No active compression exists",
      reply_to_message_id=update.message_id
    )
