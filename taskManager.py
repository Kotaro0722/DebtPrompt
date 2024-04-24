import discord
import re
import datetime

def task_manager_on_message(message:discord.Message,client:discord.Client):
    pattern_task_register="【.*】\s*[\d\d?/\d\d?\s\d\d?:\d\d]"
    is_task_register=re.fullmatch(pattern_task_register,message.content)
    
message="【(あいうえお)[http://<>]】11/11 11:11"
pattern_task_register="【.*】\d\d?/\d\d?\s\d\d?:\d\d"
is_task_register=re.fullmatch(pattern_task_register,message)
if is_task_register:
    this_year=datetime.date.today().year
    date_str=re.findall("\d\d?/\d\d?\s\d\d?:\d\d",message)[0]
    date=datetime.datetime.strptime(f"{this_year}/"+date_str,"%Y/%m/%d %H:%M")
    