from firebase import firebase
import datetime,pytz

firebase = firebase.FirebaseApplication("database url")
date=datetime.datetime.utcnow()
date2=date.replace(tzinfo=pytz.UTC)
date=date2.astimezone(pytz.timezone("Asia/Kolkata"))
date=str(date)
date=date[0:10]
today_date = int(date.replace("-", ""))

def update(chatids):
    chatid = chatids
    data = {
        "uname": chatid,
        "date": today_date
    }
    result = firebase.get('/users', chatid)
    if result:
        date = result["date"]
        if not date == today_date:
            firebase.put('/users', chatid, data)
    else:
        firebase.put('/users', chatid, data)


def status():
    users = firebase.get('/users', '')
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
