class InlineKeyboard:
    def __init__(self, bot = None):
        self.layout = {'inline_keyboard':[]}
        self.bot = bot

    def add_buttons(self, *args, handler=None):
        buttons = []
        for button in args:
            buttons.append( {'text':button, 'callback_data':button} )
            #if self.bot != None:
            #    self.bot.bind(callback_data=button, handler=handler)
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
