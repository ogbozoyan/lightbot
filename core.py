import requests
import json

class Bot:

    def __init__(self, token):
        self.token = token
        self.data = {'offset': 0, 'limit': 0, 'timeout': 0}
        self.url = f'https://api.telegram.org/bot{token}'
        self.next_step_handlers = {}

        self.event_handlers = {}

        self.command_handlers = {}  # обработчики комманд
        self.callback_handlers = {} # обработчики нажатий callback кнопок

        self.text_handler = None # управление событием 'message'
        self.location_handler = None
        self.file_handler = None
        self.callback_handler = None # управление событием 'callback'

        self.input_handlers = {}    # обработчики ввода пользователя
        self.input_cancel_handler = None # обработчик функции, которая вызывается после отмены ввода

        self.unregistred_event_handler = None
        self.unregistred_command_handler = None

        self.event = {}
        self.chat_id = ''
        self.text = ''
        self.language_code = ''

        self.location = {}

        self.photo = []
        self.document = {}
        self.document_path = './documents/'
        self.voice = {}
        self.voices_path = './voices'

    def set_polling(self):
        ''' ставим режим прослушки событий '''
        try:
            self.data = {'offset': 0, 'limit': 0, 'timeout': 0}
        except Exception as err:
            print(f'Err in set_polling: {err}')

    def send_message(self, text, keyboard = {}, parse_mode='markdown'):
        ''' Отправка сообщений '''
        try:
            message_data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'reply_markup': json.dumps(keyboard)
            }

            requests.get(f'{self.url}/sendMessage', data=message_data)

        except Exception as err:
            print(f'Err in send_message: {err}')

    def send_photo(self, photo, text = '', keyboard = {}, parse_mode='markdown'):
        ''' Отправка фотографий по url и file_id '''
        try:
            message_data = {
                'chat_id': self.chat_id,
                'photo': photo,
                'caption': text,
                'parse_mode': parse_mode,
                'reply_markup': json.dumps(keyboard)
            }

            requests.get(f'{self.url}/sendPhoto', data=message_data)

        except Exception as err:
            print(f'Err in send_message: {err}')

    def send_document(self, document, text = '', keyboard = {}, parse_mode='markdown'):
            ''' Отправка документов по url и file_id '''
            try:
                message_data = {
                    'chat_id': self.chat_id,
                    'caption': text,
                    'parse_mode': parse_mode,
                    'reply_markup': json.dumps(keyboard)
                }

                document_data = {'document': document}

                requests.get(f'{self.url}/sendDocument', data=message_data, files=document_data)

            except Exception as err:
                print(f'Err in send_message: {err}')

    def download_file(self, file_id, path=None):
        ''' скачивание файла. '''
        response = requests.get(f'{self.url}/getFile?file_id={file_id}')
        response = json.loads(response.content)
        if response['ok'] != True:
            return

        print(response)
        telegram_file_path = response['result']['file_path']
        file = requests.get(f'https://api.telegram.org/file/bot{self.token}/{telegram_file_path}')

        if path == None:
            path = telegram_file_path

        with open(path, 'wb') as doc:
            doc.write(file.content)

    def bind_command(self, command, handler, data=None):
        ''' биндит команду на конкретную функцию. '''
        self.command_handlers[command] = {'handler': handler, 'data': data}

    def bind_callback(self, command, handler, data=None):
        ''' биндит callback на конкретную функцию. '''
        self.callback_handlers[command] = {'handler': handler, 'data': data}

    def bind_event(self, event, handler, data=None):
        ''' биндит callback на конкретную функцию. '''
        self.event_handlers[event] = {'handler': handler, 'data': data}

    def bind_next_step(self, command, handler, data=None):
        '''
            биндит функцию, которая должна вызваться следующей.
            Так реализовано ветвление
        '''
        if not self.next_step_handlers.get(self.chat_id):
            self.next_step_handlers[self.chat_id] = {}

        self.next_step_handlers[self.chat_id][command] = {'handler': handler, 'data': data}

    def bind_input(self, event, handler, cancel_command=None):
        '''
            метод указывает, что следущее сообщение должно интерпритироваться как ввод документов.
            handler это функция для обработки этих данных
        '''
        if not self.input_handlers.get(self.chat_id):
            self.input_handlers[self.chat_id] = {}

        if event == 'location':
            self.input_handlers[self.chat_id]['text'] = {'event': event, 'handler': handler, 'cancel_command': None}
        if event == 'text':
            self.input_handlers[self.chat_id]['text'] = {'event': event, 'handler': handler, 'cancel_command': None}
        if event == 'photo':
            self.input_handlers[self.chat_id]['photo'] = {'event': event, 'handler': handler, 'cancel_command': None}
        if event == 'voice':
            self.input_handlers[self.chat_id]['voice'] = {'event': event, 'handler': handler, 'cancel_command': None}
        if event == 'document':
            self.input_handlers[self.chat_id]['document'] = {'event': event, 'handler': handler, 'cancel_command': None}
        #self.input_documents_handlers[self.chat_id] ={'event': event, 'handler': handler, 'cancel_command': None}

    def unregistred_event(self, event_handler):
        '''
            handler вызывается, если сообщение не является какой-либо командой
        '''
        self.unregistred_event_handler = event_handler

    def unregistred_command(self, event_handler):
        '''
            handler вызывается, если сообщение не является какой-либо командой
        '''
        self.unregistred_command_handler = event_handler

    ## IDEA: парсить поля события отдельным методом внутри этого класса

    def run(self, show_event=False):
        ''' Обработчик событий '''
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

                    if 'location' in message_event_keys  and self.location_handler != None:
                        self.process_event('location')
                        self.location_handler.set_vars(event, self)
                        self.location_handler.process(self)

                    if 'photo' in message_event_keys and self.file_handler != None:
                        self.file_handler.set_vars(event, self)
                        self.file_handler.process(self)

                    if 'document' in message_event_keys and self.file_handler != None:
                        self.file_handler.set_vars(event, self)
                        self.file_handler.process(self)

                    if 'voice' in message_event_keys and self.file_handler != None:
                        self.file_handler.set_vars(event, self)
                        self.file_handler.process(self)

                    if 'text' in message_event_keys and self.text_handler != None:
                        self.text_handler.set_vars(event, self)
                        self.text_handler.process(self)

                elif 'callback_query' in event.keys() and self.callback_handler != None:
                    self.callback_handler.set_vars(event, self)
                    self.callback_handler.process(self)

                else:
                    if self.unregistred_event_handler != None:
                        self.unregistred_event_handler()
