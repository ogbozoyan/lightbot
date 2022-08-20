<p align="center">
 <img src="https://i.imgur.com/rSyq3MW.png" alt="The Documentation Compendium"></a>
</p>

<h3 align="center">The Documentation</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![License](https://img.shields.io/badge/license-CC0-blue.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

</div>

---

<p align = "center">💡 Документация по работе с библиотекой. (Документация в разработке)</p>


## Приступим к работе

- [Авторизация бота](#bot_init)
- [Установка режима прослушки - set_polling()](#polling)
- [Установка обработчиков](#set_handlers)
- [Связываем события с функциями](#bind)
  - [Связываем команды - bind_command()](#bind_command)
  - [Связываем callback кнопки - bind_callback()](#bind_callback)
  - [Связываем события целиком - bind_event()](#bind_event)
- [Обработка событий](#events)
  - [Обработка текста и команд](#text_handler)
  - [Обработка фотографий](#photo_handler)
  - [Обработка документов](#document_handler)
  - [Обработка голосовых сообщений](#voice_handler)
  - [Обработка незарегистрированных команд](#)
  - [Обработка незарегистрированных событий](#)
- [Отправка сообщений](#send_message)
- [Работа с клавиатурами](#keyboards)
  - [Inline клавиатуры](#)
  - [Reply клавиатуры](#)
- [Ожидание события от пользователя](#)
- [Ветвление](#dialog)
- [Скачивание файлов](#download_files)
- [Обратная связь](#feedback)
- [Acknowledgements](#acknowledgements)


## Авторизация бота <a name = "bot_init"></a>

Чтобы авторизировать бота, достаточно передать его токен при создании объекта класса Bot
```python
from core import Bot
bot = Bot('55950...YoxWc')
```

## Установка режима прослушки - set_polling() <a name = "polling"></a>

Для работы бота нужно сначала установить метод взаимодействия с telegram. В настоящее время реализован только long polling, чтобы установить его, надо использовать метод set_polling() класса Bot: 

```python
bot.set_polling()
```

```python
# Пример
from core import Bot
bot = Bot('55950...YoxWc')
...
if __name__ == '__main__':
    bot.set_polling()
```

## Установка обработчиков <a name = "set_handlers"></a>

Обработчики событий - это отдельные классы, которые обрабатывают определенные события. На данный момент реализованы 4 обработчика:

- обработчик текста и команд: TextHandler
- обработчик нажатий callback кнопок: CallbackHandler
- обработчик файлов: FileHandler
- обработчик локации: LocationHandler

Для подключения надо импортировать класс обработчика и затем создать объект этого класса.

bot.text_handler
bot.file_handler
bot.callback_handler
bot.location_handler

```python
from handlers.file_handler import FileHandler
...
bot.file_handler=FileHandler()
```

```python
from handlers.text_handler import TextHandler

if __name__ == '__main__':
    bot.set_polling()
    bot.text_handler=TextHandler()
    bot.bind('/start', start_func)
```

## Связываем события с функциями <a name = "bind"></a>

Для того чтобы добавить функционал боту, надо связать действия пользователя и функции, которые будут вызываться когда пользователь это действие совершает.
Связывание происходит глобально, это значит, что команды, кнопки и события будут доступны в любом месте диалога с ботом.
Если необходимо сделать ветвление - [вот более подходящий метод](#dialog)

### Связываем команды - bind_command() <a name = "bind_command"></a>

Для связывания текстовой команды с функцией используется метод bind_command класса Bot:
```python
def bind_command(self, command, handler, data=None):
```

В параметр command передается строка с текстом, которая будет означать команду,
В параметр handler передаётся функция, которая будет вызываться по команде,
В параметр data можно передать что-то, что далее будет передаваться в функцию

Пример без передачи переменной в параметр data
```python
bot = Bot('55950...YoxWc')
...
def start_func():
    pass
    
if __name__ == '__main__':
    bot.set_polling()
    bot.bind_command('/start', start_func)
    bot.run()
```

Пример с передачей переменной в параметр data 
```python
bot = Bot('55950...YoxWc')
...
def start_func(data):
    print(data) # hello, world!
    
if __name__ == '__main__':
    bot.set_polling()
    bot.bind_command('/start', start_func, data='hello, world!')
    bot.run()
```

### Связываем callback кнопки - bind_callback() <a name = "bind_callback"></a>

Для связывания callback кнопки с функцией используется метод bind_callback класса Bot:
```python
def bind_callback(self, command, handler, data=None):
```

В параметр command передается строка с текстом кнопки,
В параметр handler передаётся функция, которая будет вызываться по нажатию этой кнопки,
В параметр data можно передать что-то, что далее будет передаваться в функцию [(См. bind_command())](#bind_command).

```python
# Пример
from handlers.callback_handler import CallbackHandler
from keyboads.keyboards import InlineKeyboard
...

bot = Bot('55950...YoxWc')
...

def button_handler():
    bot.send_message('кнопка была нажата')


def start_func():
    keyboard = InlineKeyboard()
    keyboard.add_button('кнопка')
    
    bot.send_message("Нажми на кнопку", keyboard=keyboard.layout)
    
    
if __name__ == '__main__':
    bot.set_polling()
    bot.callback_handler = CallbackHandler() # указываем обработчик callback кнопок
    bot.bind_command('/start', start_func)
    bot.bind_callback('кнопка', button_handler) # связываем кнопку и функцию, которая будет вызыватся при нажатии
```

### Связываем события целиком - bind_event()

Для связывания события с функцией используется метод bind_event класса Bot:
```python
def bind_event(self, event, handler, data=None):
```

В параметр event передается строка с названием события (См. ниже),
В параметр handler передаётся функция, которая будет вызываться по возникновению этого события,
В параметр data можно передать что-то, что далее будет передаваться в функцию [(См. bind_command())](#bind_command).

Реализованы события:
- text: когда приходит текстовое сообщение
- location: когда приходит сообщение с локацией
- photo: когда приходит фотография
- document: когда приходит документ
- voice: когда приходит голосовое сообщение

```python
# Пример
from handlers.file_handler import FileHandler
...

bot = Bot('55950...YoxWc')
...

def photo_handler():
    bot.send_message("Получена фотография")
    
if __name__ == '__main__':
    bot.set_polling()
    bot.bind_event('photo', photo_handler)
    
```


## Обработка событий <a name = "events"></a>

Написать про то, как правильно обрабатывать событие, какие переменные заполняются
```python

```
- Обработка текста и команд
- Обработка фотографий
- Обработка документов
- Обработка голосовых сообщений
- Обработка незарегистрированных команд
- Обработка незарегистрированных событий


## Отправка сообщений <a name = "send_message"></a>

Для отправки сообщений используется метод send_message класса Bot:
```python
def send_message(text, keyboard={}, ...):
```

Написать про то, что можно передать клавиатуру и задать настройки сообщения

```python
bot = Bot('55950...YoxWc')
...
def some_func():
    bot.send_message("hello, world!"):
```

**Things you should avoid:**

- Don't assume prior knowledge about the topic. If you want to appeal to a large audience, then you are going to have people with very diverse backgrounds
- Don't use idioms. Write using more formal terms that are well defined. This makes it easier for non-native English speakers and for translations to be written
- Don't clutter explanations with overly detailed examples
- Don't use terms that are offensive to any group. There will never be a good reason to


## Работа с клавиатурами <a name = "keyboards"></a>

### Inline клавиатуры

```python
from keyboards.keyboards import InlineKeyboard
...
def some_func():
    keyboard = InlineKeyboard()
    keyboard.add_buttons('btn1', 'btn2')
    keyboard.add_buttons('btn3')

    bot.send_message("hello, world", keyboard=keyboard.layout)
    
```
### Reply клавиатуры

```python
from keyboards.keyboards import ReplyKeyboard
def some_func():
    keyboard = ReplyKeyboard(one_time_keyboard=True)
    keyboard.add_buttons('btn1', 'btn2')
    keyboard.add_buttons('btn3')

    bot.send_message("hello, world", keyboard=keyboard.layout)
    
## Ожидание события от пользователя

```python
def bind_input(self, event, handler, cancel_command=None):
```

Ожидание события:
- text
- location
- photo
- document
- voice

Если задано ожидание от пользователя конкретного события, то никакое другое событие не сможет затригерить бота. Бот будет ждать только заданное событие.

```python
def some_func():
    bot.send_message("Отправь мне фотографию")
    bot.bind_input('photo', process_photo)
    

def process_photo():
    # Обработка полученной фотографии
    pass
```

Можно задать команду отмены ожидания текста, для этого надо заранее забиндить команду отмены на функцию:

```python
def some_func():
    keyboard = ReplyKeyboard(one_time_keyboard=True)
    keyboard.add_buttons('Отмена')
       
    bot.send_message("Отправь мне текст", keyboard=keyboard.layout)
    
    bot.bind_command('отмена', cancel_func)
    bot.bind_input('text', process_text, cancel_command='отмена')


def process_text():
    # Обработка полученной фотографии
    pass
    
    
def cancel_func():
    bot.send_message("Ожидание отменено")
```

## Ветвление <a name="dialog"></a>

Реализующий ветвление метод:
```python
bind_next_step(self, command, handler, data=None):
```

Регистрирует команду или callback кпонку, которая должна быть нажата дальше

```python
def some_func():

    keyboard = ReplyKeyboard()
    keyboard.add_buttons('btn1', 'btn2', 'btn3')

    bot.send_photo(file_id, text=f'Текущее расширение: {original_photo.format}', keyboard=keyboard.layout)
    
    bot.bind_next_step('btn1', btn1_handler_func)
    bot.bind_next_step('btn2', btn2_handler_func)
    bot.bind_next_step('btn3', btn3_handler_func)
    
    
def btn1_handler_func():
    pass
    
def btn2_handler_func():
    pass
    
def btn3_handler_func():
    pass
```

Если пользователь напишет одну из команд 'btn1' 'btn2' 'btn3' до вызова функции some_func, то ничего не произойдет

## Скачивание файлов

```python
download_file(self, file_id, path=None):
```
Путь сохранения файлов по умолчанию:
- голосовые сообщения скачиваются в папку voice
- документы скачиваются в папку documents
- фотографии скачиваются в папку photos

Свой путь можно задать через параметр path

## Обратная связь <a name = "feedback"></a>

- [feedmereadmes]([https://github.com/LappleApple/feedmereadmes](https://github.com/DmitriiSubpp)) - мои контакты


## Acknowledgements <a name = "acknowledgements"></a>

1. [Documenting your projects on GitHub](https://guides.github.com/features/wikis/) - GitHub Guides
2. [documentation-handbook](https://github.com/jamiebuilds/documentation-handbook) - jamiebuilds
3. [Documentation Guide](https://www.writethedocs.org/guide/) - Write the Docs


## P.S. <a name = "ps"></a>

- Этот репозиторий находится в активной разработке. Если у тебя есть предложения по улучшению, пожалуйста, воспользуйся [issue](#) или пришли свой [Pull Request](#)
