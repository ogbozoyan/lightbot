from lightbot import bot, InlineKeyboard
from PIL import Image


def unregistred_event():
    bot.send_message('No such event. Send me a photo')


def unregistred_command():
    bot.send_message('No such command. Send me a photo')


def photo():
    file_id = bot.photo[2]['file_id']

    keyboard = InlineKeyboard()
    keyboard.add_buttons('JPEG', 'BMP', 'PNG')

    file_path = bot.download_file(file_id)
    original_photo = Image.open(file_path)

    bot.send_photo(file_id, caption=f'Current format: {original_photo.format}', keyboard=keyboard.layout)
    bot.bind_event('callback', converter, data=file_path)


def converter(file_path):

    original_photo = Image.open(file_path)

    match bot.text:
        case 'JPEG':
            original_photo.save('file.jpeg', 'jpeg')
            photo_after_edit = open('file.jpeg', 'rb')
        case 'PNG':
            original_photo.save('file.png', 'png')
            photo_after_edit = open('file.png', 'rb')
        case 'BMP':
            original_photo.save('file.bmp', 'bmp')
            photo_after_edit = open('file.bmp', 'rb')

    bot.send_document(photo_after_edit)
    photo_after_edit.close()


if __name__ == '__main__':

    bot.bind_event('photo', photo)
    bot.unregistred_event(unregistred_event)
    bot.unregistred_command(unregistred_command)

    bot.run(token='5595021127:AAH9JTi2pt8UZutLSnIUhx7u2tzlU6YoxWc')
