from telegram import *

def main():
    config = get_config()
    """
    client = create_telegram_instance(config)
    print('instance created')
    channel = get_channel(client)
    print("channel created")
    """
    last_message = get_last_message()
    print(last_message)
    print(last_message["message"]["text"])




if __name__ == '__main__':
    main()