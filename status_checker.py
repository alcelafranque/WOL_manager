import os


def status_checker():
    turned_off = get_status()
    return True if turned_off else False


def get_status():
    output = os.system("ping -c 4 -q 10.240.128.69")
    print(output)
    return True if output == 0 else False