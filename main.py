import os
from flat import startflat
from consol import startconsol


def start():
    r_conf = {}
    filename = 'config.txt'
    with open(filename, encoding='utf-8') as file_object:
        conf = file_object.readlines()
        for i in conf:
            parts = i.strip().split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            r_conf[key] = value

    file_name = r_conf.get('file_name', '').strip()
    if not file_name:
        print('Error: file_name is not set in config.txt')
        return

    if r_conf.get('Graphics mode') == '+':
        startflat()
    else:
        startconsol(file_name)



if __name__ == "__main__":
    start()