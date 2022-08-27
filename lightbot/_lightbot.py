import requests
import json


class InlineKeyboard:
    def __init__(self, bot = None):
        self.layout = {'inline_keyboard':[]}
        self.bot = bot

    def add_buttons(self, *args, handler=None):
        buttons = []
        for button in args:
            buttons.append( {'text':button, 'callback_data':button} )
        self.layout['inline_keyboard'].append( buttons )


class ReplyKeyboard:
    def __init__(self, resize_keyboard=False, one_time_keyboard=False, input_field_placeholder='', selective=False):
        self.layout = {
            'keyboard': [],
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard,
            'input_field_placeholder': input_field_placeholder,
            'selective': selective
        }

    def add_buttons(self, *args):
        buttons = []
        for button in args:
            buttons.append( {'text':button} )
        self.layout['keyboard'].append( buttons )


class Core:
    def __init__(
        self,
        text_handler,
        callback_handler,
        file_handler,
        location_handler
    ):
        self.token = None
        self.data = {'offset': 0, 'limit': 0, 'timeout': 0}
        self.url = ''

        self.event_handlers = {}

        self.command_handlers = {}  # обработчики комманд
        self.callback_button_handlers = {} # обработчики нажатий callback кнопок

        self.text_handler = text_handler # управление событием 'message'
        self.location_handler = location_handler
        self.file_handler = file_handler
        self.callback_handler = callback_handler # управление событием 'callback'

        self.input_handlers = {}    # обработчики ввода пользователя
        self.input_cancel_handler = None # обработчик функции, которая вызывается после отмены ввода

        self.unregistred_event_handler = None
        self.unregistred_command_handler = None

        self.event = {}
        self.chat_id = ''
        self.message_id = ''
        self.text = ''
        self.language_code = ''

        self.location = {}

        self.photo = []
        self.document = {}
        self.document_path = './documents/'
        self.voice = {}
        self.voices_path = './voices/'

    def edit_message(self, text, keyboard={}, parse_mode='markdown'):
        r'''Edit bot\'s last message, work only with callback buttons.

        Parameters
        ----------
        text : |str|
            New text of the message. 1-4096 characters.
        keyboard : |dict|, optional
            Dictionary with reply_keyboard or inline_keyboard layout.
        parse_mode : |str|, optional
            Mode for parsing entities in the message text.
        '''
        message_data = {
            'chat_id': self.chat_id,
            'text': text,
            'message_id': self.message_id,
            'parse_mode': parse_mode,
            'reply_markup': json.dumps(keyboard)
        }

        requests.get(f'{self.url}/editMessageText', data=message_data)

    def send_message(self, text, chat_id=None, keyboard = {}, parse_mode='markdown'):
        r'''Send message to user.

        Parameters
        ----------
        text : |str|
            New text of the message. 1-4096 characters.
        chat_id : |str| or |int|, optional
            Unique identifier for the target chat.
        keyboard : |dict|, optional
            Dictionary with reply_keyboard or inline_keyboard layout.
        parse_mode : |str|, optional
            Mode for parsing entities in the message text.
        '''
        message_data = {
            'chat_id': self.chat_id if chat_id == None else chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': json.dumps(keyboard)
        }

        requests.get(f'{self.url}/sendMessage', data=message_data)

    def send_photo(self, photo, chat_id=None, caption = '', keyboard = {}, parse_mode='markdown'):
        r'''Send photo to user.

        Parameters
        ----------
        photo : |str|
            Photo to send. Pass a file_id as String to send a photo that exists
            on the Telegram servers (recommended), pass an HTTP URL as a String
            for Telegram to get a photo from the Internet, or upload a new photo
            using multipart/form-data. The photo must be at most 10 MB in size.
            The photo's width and height must not exceed 10000 in total.
            Width and height ratio must be at most 20.
        chat_id : |str| or |int|, optional
            Unique identifier for the target chat.
        caption : |str|, optional
            Photo caption, 0-1024 characters.
        keyboard : |dict|, optional
            Dictionary with reply_keyboard or inline_keyboard layout.
        parse_mode : |str|, optional
            Mode for parsing entities in the caption text.
        '''
        message_data = {
            'chat_id': self.chat_id if chat_id == None else chat_id,
            'photo': photo,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': json.dumps(keyboard)
        }

        requests.get(f'{self.url}/sendPhoto', data=message_data)


    def send_document(self, document, chat_id=None, caption = '', keyboard = {}, parse_mode='markdown'):
        r'''Send document to user.

        Parameters
        ----------
        document : |str|
            File to send. Pass a file_id as String to send a file that exists on
            the Telegram servers (recommended), pass an HTTP URL as a String for
            Telegram to get a file from the Internet, or upload a new one using
            multipart/form-data.
        chat_id : |str| or |int|, optional
            Unique identifier for the target chat.
        caption : |str|, optional
            Photo caption, 0-1024 characters.
        keyboard : |dict|, optional
            Dictionary with reply_keyboard or inline_keyboard layout.
        parse_mode : |str|, optional
            Mode for parsing entities in the caption text.
        '''
        message_data = {
            'chat_id': self.chat_id if chat_id == None else chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': json.dumps(keyboard)
        }

        document_data = {'document': document}
        requests.get(f'{self.url}/sendDocument', data=message_data, files=document_data)


    def download_file(self, file_id, path=None):
        r'''Download photo, voice message, document from telegram.

        Parameters
        ----------
        file_id : |str|
            File identifier of file to be downloaded.
        path : |str|, optional
            Custom file name. default paths:
                for photos: ./photos/
                for voice: ./voice/
                for documents: ./documents/
        '''
        response = requests.get(f'{self.url}/getFile?file_id={file_id}')
        response = json.loads(response.content)
        if response['ok'] != True:
            return

        telegram_file_path = response['result']['file_path']
        file = requests.get(f'https://api.telegram.org/file/bot{self.token}/{telegram_file_path}')

        if path == None:
            path = telegram_file_path

        with open(path, 'wb') as doc:
            doc.write(file.content)

    def bind_command(self, command, handler, data=None):
        r'''Bind command to the handler function.

        Parameters
        ----------
        command : |str|
            Command to bind. When bot get this command from user, handler
            function will be invoked.
        handler : |function|
            Function that will be invoked when bot gets command from user.
        data : |str|, optional
            Data to be passed to the function.
        '''
        self.command_handlers[command] = {'handler': handler, 'data': data}

    def bind_callback(self, callback_data, handler, data=None):
        r'''Bind callback button to the handler function.

        Parameters
        ----------
        callback_data : |str|
            callback_data to bind. When bot get this callback data from user, handler
            function will be invoked.
        handler : |function|
            Function that will be invoked when user pressed callback button.
        data : |str|, optional
            Data to be passed to the function.
        '''
        self.callback_button_handlers[callback_data] = {'handler': handler, 'data': data}

    def bind_event(self, event, handler, data=None):
        r'''Bind event to the handler function.

        Parameters
        ----------
        event : |str|
            Event to bind. When bot get this event from user, handler
            function will be invoked.
            Available events:
                text,
                callback,
                location,
                photo,
                document,
                voice
        handler : |function|
            Function that will be invoked when user arise event.
        data : |str|, optional
            Data to be passed to the function.
        '''
        self.event_handlers[event] = {'handler': handler, 'data': data}

    def bind_input(self, event, handler, cancel_command=None, data=None):
        r'''Get user input and bind it to the handler function. This method
        can be used for create a dialog tree.

        Parameters
        ----------
        event : |str|
            Event to bind. When bot get this event from user, handler
            function will be invoked.
            Available events:
                text,
                callback,
                location,
                photo,
                document,
                voice
        handler : |function|
            Function that will be invoked when user arise event.
        cancel_command : |str|
            Command or callback_data whitch stop input - in development
        data : |str|, optional
            Data to be passed to the function.
        '''
        self.input_handlers.setdefault(self.chat_id, {})

        if event == 'callback':
            self.input_handlers[self.chat_id]['callback'] = {
                'handler': handler,
                'cancel_command': cancel_command,
                'data': data
            }
        if event == 'location':
            self.input_handlers[self.chat_id]['location'] = {
                'handler': handler,
                'cancel_command': cancel_command,
                'data': data
            }
        if event == 'text':
            self.input_handlers[self.chat_id]['text'] = {
                'handler': handler,
                'cancel_command': cancel_command,
                'data': data
            }
        if event == 'photo':
            self.input_handlers[self.chat_id]['photo'] = {
                'handler': handler,
                'cancel_command': cancel_command,
                'data': data
            }
        if event == 'voice':
            self.input_handlers[self.chat_id]['voice'] = {
                'handler': handler,
                'cancel_command': cancel_command,
                'data': data
            }
        if event == 'document':
            self.input_handlers[self.chat_id]['document'] = {
                'handler': handler,
                'cancel_command': cancel_command,
                'data': data
            }

    def unregistred_event(self, handler):
        r'''Bind function for event, which has not been binded before.

        Parameters
        ----------
        handler : |function|
            Function that will be invoked when unregistred event arise.
        '''
        self.unregistred_event_handler = handler

    def unregistred_command(self, handler):
        r'''Bind function for command ot text, which has not been binded before.

        Parameters
        ----------
        handler : |function|
            Function that will be invoked when user send unregistred command or text.
        '''
        self.unregistred_command_handler = handler


    def run(self, token='', show_event=False):
        r'''Starts listening to events.

        Parameters
        ----------
        token: |str|
            Unique authentication token.
            The token looks something like 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
        show_event : |bool|
            If true, prints event to console.
        '''

        self.token = token
        self.url = f'https://api.telegram.org/bot{token}'

        while(True):
            updates = requests.get(f'{self.url}/getUpdates', data=self.data)
            events = updates.json()['result']

            for event in events:

                if (show_event):
                    print(event)

                self.data['offset'] = event['update_id'] + 1

                self.event = event

                if 'message' in event.keys():
                    message_event_keys = event['message'].keys()

                    if 'location' in message_event_keys:
                        self.location_handler.set_vars(event, self)
                        self.location_handler.process(self)

                    if 'photo' in message_event_keys:
                        self.file_handler.set_vars(event, self)
                        self.file_handler.process(self)

                    if 'document' in message_event_keys:
                        self.file_handler.set_vars(event, self)
                        self.file_handler.process(self)

                    if 'voice' in message_event_keys:
                        self.file_handler.set_vars(event, self)
                        self.file_handler.process(self)

                    if 'text' in message_event_keys:
                        self.text_handler.set_vars(event, self)
                        self.text_handler.process(self)

                elif 'callback_query' in event.keys():
                    self.callback_handler.set_vars(event, self)
                    self.callback_handler.process(self)

                else:
                    if self.unregistred_event_handler != None:
                        self.unregistred_event_handler()
