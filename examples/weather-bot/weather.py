import requests
from lightbot import bot, InlineKeyboard


def start():
    help_en = 'Send me your location and I will tell about weather in your region\n\n'
    bot.send_message(help_en)


def getWeather_by_coord(location, lang):
    URL = f"""https://api.openweathermap.org/data/2.5/weather?lat={location['latitude']}&lon={location['longitude']}&appid=a4ffa...306cc7&lang={lang}&units=metric"""

    response = requests.get(URL).json()
    if response['cod'] == 200:
        return response, 200
    else:
        return '', response['cod']


def get_weather():
    response, code = getWeather_by_coord(bot.location, bot.language_code)
    if code == 200:
        text = f"Температура: {response['main']['temp']}°   \
                \nОщущается как: {response['main']['feels_like']}° \
                \nДавление: {response['main']['pressure']} hPa     \
                \nЛокация: {response['name']}"
        bot.send_message(text)
    else:
        bot.send_message('Sity not found')


if __name__ == '__main__':

    bot.bind_command('/help', start)
    bot.bind_command('/start', start)

    bot.bind_event('location', get_weather)

    bot.run(token='55950...YoxWc')
