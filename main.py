import telebot
import re
from tld import is_tld
import bot_token


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
    new_users.add(message.from_user.id)


@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.from_user.id in new_users:
        new_users.discard(message.from_user.id)
        urls = get_valid_urls(message.text)
        body = "I've deleted spam with this urls: "
        # print(urls)
        if len(urls):
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, body + ", ".join(urls))


bot.polling()
