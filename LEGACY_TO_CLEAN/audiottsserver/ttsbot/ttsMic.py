#mAlc_Jke \ vya4es.ru/projects/txt-to-speech-mic

import gtts
import pygame
import os
import glob

from time import sleep
from pydub import AudioSegment
from pygame import mixer, _sdl2 as devices


# The list of display text in diferent languages
'''device_output_text={
    'es': 'Dispositivos de entrada de audio disponibles',
    'en': 'Available audio input devices:',
    'ru': 'Доступные аудио-входные устройства:'
}

choices_output_text={
    'es': 'Escoge uno: ',
    'en': 'Choose one: ',
    'ru': 'Выберите один: '
}

choices_incorrect_by_number_output_text={
    'es': 'Solo uno de los ',
    'en': 'Just one of them ',
    'ru': 'Выберите один из '
}

choices_incorrect_by_value_output_text={
    'es': 'Valor incorrecto ingrese nuevamente ',
    'en': 'Incorrect value, try again ',
    'ru': 'Неверное значение, попробуйте еще раз '
}'''

insert_output_text={
    'es': 'Ingrese el texto a hablar: ',
    'en': 'Enter the text to speak: ',
    'ru': 'Введите текст для озвучивания: '
}

def play(file_path: str, device: str):
    if device is None:
        devices = get_devices()
        if not devices:
            raise RuntimeError("No device!")
        device = devices[0]
    #print("Play: {}\r\nDevice: {}".format(file_path, device))
    pygame.mixer.init(devicename=device)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    duration = get_audio_duration(file_path)
    sleep(duration)
    pygame.mixer.quit()

def text_to_speech(text,language):
    tts = gtts.gTTS(text, lang=language)
    tts.save('temp.mp3')

def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_in_seconds = len(audio) / 1000  # Преобразование миллисекунд в секунды
    return duration_in_seconds

def get_audio_input_device(language):
    mixer.init()  # Инициализация mixer
    audio_devices = devices.audio.get_audio_device_names(False)  # Получение всех доступных аудио-входных устройств

    preferred_device = "Steam Streaming Microphone"

    print('Available audio input devices:')
    for i, device in enumerate(audio_devices):
        print(f"{i+1}. {device}")

        if device == preferred_device:
            selected_device = audio_devices[i]  # Выбор указанного устройства
            mixer.quit()
            return selected_device

        else:
            pass

    
    

    raise ValueError("Sorry that mic doesn't exist. Look at the available ones above")



def setup():

    language = 'en'
    selected_device = get_audio_input_device(language)

    return selected_device
    # input_path = "inputs/"

    # for file_path in glob.glob(os.path.join(input_path, "*.txt")):
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         file_name = os.path.basename(file_path)
    #         text = file.read()
    #         print(f"Playing {file_name}:\n{text}")
            

def inject(string, device):
    text_to_speech(string, "en")
    play('temp.mp3', device)





    '''while True:
        text = input(insert_output_text[language])
        # i think pressing ctrol + C is better than typing 'выход'
        if text.lower() == 'выход':
            break

        text_to_speech(text,language)

        # Воспроизведение сохраненной речи через виртуальный микрофон
        play('temp.mp3', selected_device)'''


