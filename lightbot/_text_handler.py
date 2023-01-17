from loguru import logger

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

    def set_vars(self, event, bot):
        r'''Parse event fields and set necessary variables.

        Parameters
        ----------
        event : |dict|
            Dictionary to parse.
        bot : |Core object|
            Main object.
        '''
        if 'text' in event['message'].keys():
            self.event = event
            self.chat_id = bot.chat_id = event['message']['from']['id']
            self.language_code = event['message']['from']['language_code']
            self.text = bot.text = event['message']['text']
            self.message_id = bot.message_id = event['message']['message_id']


    def __process_text(self, command_handlers):
        '''Invoke callback function.'''
        if command := command_handlers.get(self.text):
            try:
                command['handler']()
            except TypeError:
                loguru.error(f'There is no funtion bind for {self.text} command')

    def __process_input(self, input_text_handlers):
        '''Invoke input functions for specific type of input.'''
        if input_text_handlers.get(self.chat_id):
            if input_text_handlers[self.chat_id]['text']['cancel_command'] == self.text:
                input_text_handlers.pop(self.chat_id)
            else:
                func = input_text_handlers[self.chat_id]['text']['handler']
                data = input_text_handlers[self.chat_id]['text']['data']
                input_text_handlers.pop(self.chat_id)
                func() if data is None else func(data)

    def process(self, bot):
        '''Process event.'''

        # if bot waits for user input
        if bot.input_handlers.get(self.chat_id):
            if bot.input_handlers[self.chat_id].get('text'):
                self.__process_input(bot.input_handlers)
                return
            # cancel_command here
            return

        # if text event arise
        if bot.event_handlers.get('text'):
            func = bot.event_handlers['text']['handler']
            data = bot.event_handlers['text']['data']
            func() if data is None else func(data)
            return

        # if user typed command or text
        if bot.command_handlers.get(self.text):
            self.__process_text(bot.command_handlers)
            return

        # if unregistred command
        if bot.unregistred_command_handler != None:
            bot.unregistred_command_handler()
