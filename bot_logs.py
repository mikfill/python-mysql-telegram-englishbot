from datetime import datetime
from os import get_terminal_size
from terminal_colors import CEND, CYELLOW, CGREEN, CBLUE, CBEIGE


def log_incoming_message(word: str, chat_id: int) -> None:
    """Logging into terminal incoming word from user
    """
    print(CBLUE + f'{"=" * get_terminal_size().columns}' + CEND)
    print(
        CGREEN + f'[>>>>>] Message Recieved: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + CEND)
    print(CGREEN + f'\tText: {word}' + CEND)
    print(CGREEN + f'\tChatID: {chat_id}' + CEND)
    print(CYELLOW + f'{"=" * get_terminal_size().columns}' + CEND)


def log_outgoing_message(msg: str, chat_id: int) -> None:
    """Logging into terminal outgoing message with sentences
    """
    print(CBLUE + f'{"=" * get_terminal_size().columns}' + CEND)
    print(
        CGREEN + f'[<<<<<] Message Send: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + CEND)
    print(CGREEN + f'\tChatID: {chat_id}' + CEND)
    print(CBEIGE + f'\n{msg}' + CEND)
    print(CYELLOW + f'{"=" * get_terminal_size().columns}' + CEND)
