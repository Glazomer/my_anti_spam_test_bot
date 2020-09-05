import re
from datetime import datetime
import telebot
from tld import is_tld
import bot_token


def log(info: str):
    print(str(datetime.now()) + ': ' + info)


def get_valid_urls(string):
    regex = r"((?:https?://)?[A-Za-z0-9_\-]+\.([A-Za-z0-9_\-\.]+))"
    urls = re.findall(regex, string)  # Find anything that look like URL
    valid_urls = list()
    for el in urls:
        if is_tld(el[1]):  # el[1] is match group 1, it supposed to be
            valid_urls.append(el[0])  # if top level domain (el[1]) if valid, so url (el[0]) is
    return valid_urls


new_users = set()
bot = telebot.TeleBot(bot_token.BOT_TOKEN)  # I DON'T KNOW HOW TO EXPORT STRING IN PYTHON, SORRY!


@bot.message_handler(content_types=["new_chat_members"])
def print_all(message):
    user_id = message.from_user.id
    if user_id not in new_users:
        new_users.add(user_id)
        log(f'Added {user_id} to new_users list.')
    else:
        log(f'User {user_id} already in new_users list.')


@bot.message_handler(content_types=["text"])
def send_text(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    chat_id = message.chat.id
    msg_id = message.message_id
    msg_text = message.text
    if user_id in new_users:
        log(f'Received first message {msg_id}: "{msg_text}" from "{user_id}".')
        new_users.discard(user_id)
        urls = get_valid_urls(msg_text)
        if len(urls):
            log(f'Found these urls: "{str(urls)}" in {msg_id} ("{msg_text}").')

            log(f'Deleting message {msg_id} from chat {chat_id}.')
            bot.delete_message(chat_id, msg_id)

            log(f'Kicking user {user_id} (@{user_name}) from chat {chat_id}.')
            bot.kick_chat_member(chat_id, user_id)

            admins = bot.get_chat_administrators(chat_id)
            creator = next((member for member in admins if member.status == 'creator'), [False])
            if creator:
                bot.send_message(chat_id, f"I've just kicked {user_id} (@{user_name}). cc: @{creator.user.username}")

        else:
            log(f'Found no urls in {msg_id} ("{msg_text}").')


bot.polling()
