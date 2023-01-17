from loguru import logger

class CallbackHandler:
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
        self.event = event
        self.chat_id = bot.chat_id = event['callback_query']['from']['id']
        self.text = bot.text = event['callback_query']['data']
        self.message_id = bot.message_id = event['callback_query']['message']['message_id']

    def __process_commands(self, callback_button_handlers):
        '''Invoke callback function.'''
        if command := callback_button_handlers.get(self.text):
            try:
                command['handler']()
            except TypeError:
                loguru.error(f'There is no funtion bind for {self.text} command')

    def __process_input(self, input_handlers):
        '''Invoke input functions for specific type of input.'''
        if input_handlers.get(self.chat_id):
            if input_handlers[self.chat_id]['callback']['cancel_command'] == self.text:
                input_handlers.pop(self.chat_id)
            else:
                func = input_handlers[self.chat_id]['callback']['handler']
                data = input_handlers[self.chat_id]['callback']['data']
                input_handlers.pop(self.chat_id)
                func() if data is None else func(data)

    def process(self, bot):
        '''Process event.'''

        # if bot waits for user input
        if bot.input_handlers.get(self.chat_id):
            if bot.input_handlers[self.chat_id].get('callback'):
                self.__process_input(bot.input_handlers)
                return
            # cancel_command here
            return

        # if callback event arise
        if bot.event_handlers.get('callback'):
            func = bot.event_handlers['callback']['handler']
            data = bot.event_handlers['callback']['data']
            func() if data is None else func(data)
            return

        # if user pressed callback button
        if bot.callback_button_handlers.get(self.text):
            self.__process_commands(bot.callback_button_handlers)
            return

        # if unregistred command
        if bot.unregistred_command_handler != None:
            bot.unregistred_command_handler()
