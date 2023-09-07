import cv2
import time
import requests
from decouple import config

def main():
  while 1:
    cameraId = 1 # 0 - front laptop webcam, 1 - second usb webcam
    cap = cv2.VideoCapture(cameraId)

    if not cap.isOpened():
        message = "Не удалось открыть камеру."
        sendMessage(message, config("CHAT_ID"))
        print(message)
    else:
        ret, frame = cap.read()
        if ret:
            fileName = 'snapshot.jpg'
            cv2.imwrite(fileName, frame)
            sendPhoto(fileName, config("CHAT_ID"))
        else:
            message = "Не удалось получить кадр с камеры."
            sendMessage(message, config("CHAT_ID"))
            print(message)
        cap.release()

    time.sleep(1 * 5)

def sendPhoto(photo: str, chatId: str):
    try:
        url = f'https://api.telegram.org/bot{config("TELEGRAM_BOT_TOKEN")}/sendPhoto'
        files = {'photo': open(photo, 'rb')}
        data = {'chat_id': chatId}
        response = requests.post(url, files=files, data=data)
    except Exception as e:
        _ = 0

def sendMessage(text: str, chatId: str):
    try:
        url = f'https://api.telegram.org/bot{config("TELEGRAM_BOT_TOKEN")}/sendMessage'
        data = {'chat_id': chatId, 'text': text}
        response = requests.post(url, data=data)
    except Exception as e:
        _ = 0 

main()
