class FileHandler:
    '''docstring for MessageHandler.'''

    def __init__(self):
        self.update_id = 0
        self.message_id = 0
        self.id = 0
        self.is_bot = False
        self.first_name = ''
        self.last_name = ''
        self.username = ''
        self.language_code = ''
        self.date = 0
        self.chat_id = ''
        self.event = {}

        self.current_event = ''

        self.photo = []
        self.document = {}
        self.voice = {}

    def set_vars(self, event, bot):

        self.event = event
        self.chat_id = bot.chat_id = event['message']['from']['id']
        self.language_code = event['message']['from']['language_code']

        if 'photo' in event['message'].keys():
            self.current_event = 'photo'
            self.photo = bot.photo = event['message']['photo']

        if 'document' in event['message'].keys():
            self.current_event = 'document'
            self.document = bot.document = event['message']['document']

        if 'voice' in event['message'].keys():
            self.current_event = 'document'
            self.voice = bot.voice = event['message']['voice']

    def process_documents_input(self, input_documents_handlers, event_type):

        if event_type == 'photo':
            if input_documents_handlers.get(self.chat_id):
                #if input_handlers[self.chat_id]['cancel_command'] == self.text:
                #    input_handlers.pop(self.chat_id)
                #else:
                    func = input_documents_handlers.pop(self.chat_id)
                    func['photo']['handler']()

        if event_type == 'voice':
            if input_documents_handlers.get(self.chat_id):
                #if input_handlers[self.chat_id]['cancel_command'] == self.text:
                #    input_handlers.pop(self.chat_id)
                #else:
                    func = input_documents_handlers.pop(self.chat_id)
                    func['voice']['handler']()

        if event_type == 'document':
            if input_documents_handlers.get(self.chat_id):
                #if input_handlers[self.chat_id]['cancel_command'] == self.text:
                #    input_handlers.pop(self.chat_id)
                #else:
                    func = input_documents_handlers.pop(self.chat_id)
                    func['document']['handler']()


    def process(self, bot):

        # если бот ожидает ввода от chat_id
        if bot.input_handlers.get(self.chat_id):
            if bot.input_handlers[self.chat_id].get('photo'):
                self.process_documents_input(bot.input_handlers, 'photo')
                return
            if bot.input_handlers[self.chat_id].get('voice'):
                self.process_documents_input(bot.input_handlers, 'voice')
                return
            if bot.input_handlers[self.chat_id].get('document'):
                self.process_documents_input(bot.input_handlers, 'document')
                return
            return

        if bot.event_handlers.get('photo') and 'photo' in self.event['message'].keys():
            func = bot.event_handlers['photo']['handler']
            data = bot.event_handlers['photo']['data']
            func() if data == None else func(data)
            return

        if bot.event_handlers.get('document') and 'document' in self.event['message'].keys():
            func = bot.event_handlers['document']['handler']
            data = bot.event_handlers['document']['data']
            func() if data == None else func(data)
            return

        if bot.event_handlers.get('voice') and 'voice' in self.event['message'].keys():
            func = bot.event_handlers['voice']['handler']
            data = bot.event_handlers['voice']['data']
            func() if data == None else func(data)
            return
