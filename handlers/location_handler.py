class LocationHandler:
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
        self.location = {}

    def set_vars(self, event, bot):
        if 'location' in event['message'].keys():
            self.event = event
            self.chat_id = bot.chat_id = event['message']['from']['id']
            self.language_code = event['message']['from']['language_code']
            self.location = bot.location = event['message']['location']

    def process(self, bot):#event_handlers, input_handlers, command_handlers, next_step_handlers, other_event_handler):

        if bot.event_handlers.get('location'):
            func = bot.event_handlers['location']['handler']
            data = bot.event_handlers['location']['data']
            func() if data == None else func(data)
            return
