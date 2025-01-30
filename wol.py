def handler(event, context):
    text = 'Приветик, данный сценарий включит твой компьютер.'
    if 'request' in event and \
            'original_utterance' in event['request'] and \
            len(event['request']['original_utterance']) > 0:
        send_wol_packet()
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            # Завершение сессии после этого ответа
            'end_session': 'true'
        },
    }

# Содержание функции send_wol_packet
import socket

# Замените 'example.com' на ваш DNS или IP-адрес устройства
DEVICE_NAME = 'example.com'

# MAC-адрес устройства. Замените '00:B0:D0:61:C2:D3' на ваш MAC-адрес
MAC_ADDRESS = '00:B0:D0:61:C2:D3'

# Порт, на который отправляется WOL-пакет. Обычно это 9
PORT = 9

def send_wol_packet():
    # Преобразование DNS имени в IP-адрес
    try:
        resolved_ip = socket.gethostbyname(DEVICE_NAME)
    except socket.gaierror:
        print(f"Не удалось разрешить DNS имя: {DEVICE_NAME}")
        return

    # Проверка и преобразование MAC-адреса
    mac_address = MAC_ADDRESS.replace('-', ':')
    if len(mac_address) == 17 and mac_address.count(':') == 5:
        mac_bytes = bytes.fromhex(mac_address.replace(':', ''))
    else:
        print("Неправильный формат MAC-адреса.")
        return

    # Создание magic packet
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    # Отправка magic packet на IP-адрес
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (resolved_ip, PORT))

# Пример использования функции
send_wol_packet()
