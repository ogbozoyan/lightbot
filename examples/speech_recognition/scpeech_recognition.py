import speech_recognition as sr
import subprocess
import ffmpeg
import os
from lightbot import bot


def on_voice():

    bot.download_file(bot.voice['file_id'], './voice.opus')

    process = subprocess.run(
        ['./ffmpeg', '-i', './voice.opus', './voice.wav'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )

    if not process.returncode:
        r = sr.Recognizer()
        voice = sr.AudioFile('voice.wav')
        with voice as source:
            audio = r.record(source)
            if recognized_data := r.recognize_google(
                audio, language='ru', show_all=True
            ):
                recognized_text = recognized_data['alternative'][0]['transcript']
            else:
                recognized_text = 'None'

        bot.send_message(recognized_text)

        os.remove('./voice.wav')
        os.remove('./voice.opus')


if __name__ == '__main__':
    bot.bind_event('voice', on_voice)
    bot.run(token="", show_event=True)
