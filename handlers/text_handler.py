

class TextHandler:
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
        self.text = ''

        self.location = {}

    def set_vars(self, event, bot):
        if 'text' in event['message'].keys():
            self.event = event
            self.chat_id = bot.chat_id = event['message']['from']['id']
            self.language_code = event['message']['from']['language_code']
            self.text = bot.text = event['message']['text']


        elif 'location' in event['message'].keys():
            self.event = event
            self.chat_id = bot.chat_id = event['message']['from']['id']
            self.language_code = bot.language_code = event['message']['from']['language_code']
            self.location = bot.location = event['message']['location']


    def process_commands(self, command_handlers):
        print(command_handlers)
        handler = command_handlers.get(self.text)
        if handler:
            handler['handler']()
        else:
            pass

    def process_input(self, input_handlers):
        if input_handlers.get(self.chat_id):
            if input_handlers[self.chat_id]['text']['cancel_command'] == self.text:
                input_handlers.pop(self.chat_id)
            else:
                func = input_handlers[self.chat_id]['text']['handler']
                data = input_handlers[self.chat_id]['text']['data']
                input_handlers.pop(self.chat_id)
                func() if data == None else func(data)

    def process(self, bot):#event_handlers, input_handlers, command_handlers, next_step_handlers, other_event_handler):


        # если бот ожидает ввода от chat_id
        if bot.input_handlers.get(self.chat_id):
            if bot.input_handlers[self.chat_id].get('text'):
                self.process_input(bot.input_handlers)
                return
            # cancel_command здесь
            return

        if bot.event_handlers.get('text'):
            func = bot.event_handlers['text']['handler']
            data = bot.event_handlers['text']['data']
            func() if data == None else func(data)
            return

        # если пользователь ввел команду
        if bot.command_handlers.get(self.text):
            self.process_commands(bot.command_handlers)
            return

        # если комманды нет в списке комманд
        if bot.unregistred_command_handler != None:
            bot.unregistred_command_handler()
