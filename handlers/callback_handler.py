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

        self.event = event
        self.chat_id = bot.chat_id = event['callback_query']['from']['id']
        self.text = bot.text = event['callback_query']['data']

    def process_commands(self, callback_handlers):
        handler = callback_handlers.get(self.text)
        if handler:
            handler['handler']()
        else:
            pass

    def process_input(self, input_handlers):
        if input_handlers.get(self.chat_id):
            if input_handlers[self.chat_id]['cancel_command'] == self.text:
                input_handlers.pop(self.chat_id)
            else:
                func = input_handlers.pop(self.chat_id)
                func['handler'](self.text)

    def process_next_step_handlers(self, next_step_handlers):
        if next_step_handlers.get(self.chat_id):
            if next_step_handlers[self.chat_id].get(self.text):
                func = next_step_handlers[self.chat_id][self.text]['handler']
                data = next_step_handlers[self.chat_id][self.text]['data']
                func() if data == None else func(data)
                del(next_step_handlers[self.chat_id])

    def process(self, bot):

        # если бот ожидает ввода от chat_id
        if bot.input_handlers.get(self.chat_id):
            if bot.input_handlers[self.chat_id].get('text'):
                self.process_input(bot.input_handlers)
                return
            # cancel_command здесь
            return

        # если очередь вызова функций не пуста
        if bot.next_step_handlers.get(self.chat_id):
            if bot.next_step_handlers[self.chat_id].get(self.text):
                self.process_next_step_handlers(bot.next_step_handlers)
                return

        # если пользователь ввел команду
        if bot.command_handlers.get(self.text):
            self.process_commands(bot.command_handlers)
            return

        # если комманды нет в списке комманд
        if bot.unregistred_command_handler != None:
            bot.unregistred_command_handler()
