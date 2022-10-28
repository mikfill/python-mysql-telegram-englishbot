import json
from os import getenv
from datetime import datetime
from time import sleep
import requests
from bot_logs import log_incoming_message, log_outgoing_message
from sentences import load_sentences_local
from sentences import load_sentences_remote


def get_bot_info(bot_url: str) -> json:
    """Get basic info about bot
    """
    url = f"{bot_url}/getMe"
    response = requests.get(url, timeout=10)
    return response.json()


def get_query_url(token_env_name: str) -> str:
    """Create request url for bot

    Get telegram bot token and root url from Env variables
    export ROOT_URL=https://api.telegram.org/bot\n
    export BOT_TOKEN1=yourbottoken\n
    export BOT_TOKEN2=yourbottoken
    """

    token = getenv(token_env_name)
    root_url = getenv('ROOT_URL')

    if not token:
        raise ValueError(f"Dont have env variable with name {token_env_name}")

    query_url = f"{root_url}{token}"

    return query_url


def bot_set_commands(bot_url: str):
    """Set menu with avaliable comands for bot 
    returns http status code
    """
    url = f'{bot_url}/setMyCommands?commands='
    commands=[
    {
        "command": "start",
        "description": "Say hello from bot"
    },
    {
        "command": "hello",
        "description": "Send your current id and time"
    },
    {
        "command": "time",
        "description": "Send your id and time"
    },
    {
        "command": "help",
        "description": "Print help message to user"
    },
    {
        "command": "getlvl",
        "description": "Print current level of user"
    },
    {
        "command": "setlvl",
        "description": "Set level to user"
    }
    ]
    commands = json.dumps(commands)
    url = url + str(commands)
    response = requests.post(url, timeout=5)
    return response.status_code


def get_bot_updates(bot_url: str) -> dict:
    """Get bot updates return None if no updates available
    """
    url = f"{bot_url}/getUpdates"
    response = requests.get(url, timeout=5)
    updates = response.json()

    if updates['ok'] == True and updates['result']:
        return updates
    else:
        return {'ok': False, 'result': []}


def parse_message(update) -> tuple:
    """Get message_id, chat_id and text from bot update
    and check if update is command
    """
    is_command = False
    message_id = update['result'][-1]['message']['message_id']
    chat_id = update['result'][-1]['message']['chat'].get('id')
    txt = update['result'][-1]['message'].get('text')

    if update['result'][-1]['message'].get('entities'):
        type_of_entity = update['result'][-1]['message']['entities'][-1].get(
            'type')
        if type_of_entity == 'bot_command':
            is_command = True

    return is_command, message_id, chat_id, txt


def command_handler(bot_url: str, command: str, chat_id: int):
    """Processing bot commands received from chat
    """
    print(f"User {chat_id} send command {command} to bot")

    if command == '/start':
        start_message = "Hello from be dev english bot!\nToday we learn some english words"
        send_message(bot_url, chat_id, start_message)
        print("Bot send start message")

    if command == '/hello':
        hello_msg = f"Hello user!\nYour id:{chat_id}"
        
        send_message(bot_url, chat_id, hello_msg)
        print("Bot say hello")

    if command == '/help':
        # Call help

        print("Print text with instructions")

    if command == '/getlvl':
        # Change lvl for user
        print("Command to show lvl user")

    if command == '/setlvl':
        # Set lvl for user
        print("Command to change lvl user")

    if command == '/max':
        # Set max generation sentences
        print("Set max sentences")

    if command == '/time':
        c_time = datetime.now().strftime('%H:%M:%S')
        time_msg = f"👋: {chat_id}\n⏰:{c_time}"
        send_message(bot_url, chat_id, time_msg)
        print("Bot send time")

def send_message(bot_url: str, chat_id: int, msg: str):
    """Send message to user with chat id
    returns status code 200 if ok
    """

    url = f"{bot_url}/sendMessage"
    response = requests.post(url, json={'chat_id': chat_id, 'text': msg}, timeout=5)

    return response.status_code


def bot_echo_polling(bot_url: str, polling_interval=1):
    """Check bot update for new messages and
    sends an echo message to the user
    default polling interval 1 second
    """

    last_message_id = 0
    last_message_text = ''

    while True:
        bot_updates = get_bot_updates(bot_url)
        try:
            is_command, message_id, chat_id, txt = parse_message(bot_updates)

            if message_id > last_message_id and txt != last_message_text and is_command == False:
                last_message_id = message_id
                last_message_text = txt
                send_message(bot_url, chat_id, txt)
                print(f'Send echo {txt} to user')
            else:
                print("Polling...")
                sleep(polling_interval)
        except:
            sleep(5)
            print('Dont have updates, send something to bot!')


def get_sentences_from_local(word: str) -> str:
    """Get sentences from local sentences.py file

    return string with matched sentences with user word
    """

    list_sentences = []
    matched_sentences = []
    result_msg = ''

    list_sentences = load_sentences_local()
    for sentence in list_sentences:
        text_from_sentence = sentence.get('text')
        if word.lower() in text_from_sentence.lower():
            matched_sentences.append(text_from_sentence)

    if len(matched_sentences) == 0:
        result_msg += "No matches"
    if len(matched_sentences) == 1:
        result_msg += matched_sentences[0]
    if len(matched_sentences) > 1:
        for match in matched_sentences:
            result_msg += match + "\n...\n"

    return result_msg


def get_sentences_from_remote(word: str, amount=3) -> str:
    """Get sentences from web site
    https://sentence.yourdictionary.com/{word}
    Optionally you can specify the number of examples
    in "amount" input argument default 3

    return string with matched sentences with user word
    """

    list_sentences = []
    matched_sentences = []
    result_msg = ''

    list_sentences = load_sentences_remote(word)[:amount]
    for sentence in list_sentences:
        matched_sentences.append(sentence['text'])

    if len(matched_sentences) == 0:
        result_msg += "No matches"
    if len(matched_sentences) == 1:
        result_msg += matched_sentences[0]
    if len(matched_sentences) > 1:
        for match in matched_sentences:
            result_msg += match + "\n...\n"

    return result_msg


def bot_send_sentences(bot_url: str, polling_interval=1, remote=False):
    """Check bot update for new messages and
    send to user sentences with word inputed to chat
    default polling interval 1 second
    default load sentences from local file sentences.py
    """

    last_message_id = 0
    last_message_text = ''
    result_msg = ''

    while True:
        bot_updates = get_bot_updates(bot_url)
        try:
            is_command, message_id, chat_id, word = parse_message(bot_updates)

            if message_id > last_message_id and is_command:
                last_message_id = message_id
                command_handler(bot_url, word, chat_id)

            if not remote:
                if message_id > last_message_id and word != last_message_text and not is_command:
                    last_message_id = message_id
                    last_message_text = word
                    log_incoming_message(word, chat_id)

                    result_msg = get_sentences_from_local(word)
                    send_message(bot_url, chat_id, result_msg)

                    log_outgoing_message(result_msg, chat_id)

                else:
                    print("Polling...")
                    sleep(polling_interval)
            else:
                if message_id > last_message_id and word != last_message_text and not is_command:
                    max_number_of_sentences = 5
                    last_message_id = message_id
                    last_message_text = word
                    log_incoming_message(word, chat_id)

                    result_msg = get_sentences_from_remote(
                        word, max_number_of_sentences)
                    send_message(bot_url, chat_id, result_msg)

                    log_outgoing_message(result_msg, chat_id)

                else:
                    print("Polling...")
                    sleep(polling_interval)
        except:
            print("Dont have updates, send something to bot!")
            sleep(5)
