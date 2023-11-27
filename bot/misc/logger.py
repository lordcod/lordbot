import time

class text_colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OBLIQUE = '\033[3m'
    
    GREY = '\033[90m'#
    RED = '\033[91m'#
    GREEN = '\033[92m'#
    YELLOW = '\033[93m'#
    BLUE = '\033[94m'#
    VIOLET = '\033[95m'#
    CYAN = '\033[96m'

@lambda cls: cls()
class Logger:
    def __init__(self, service=True, date=True) -> None:
        self.service = service
        self.date = date
        pass
    
    def callback(self, text):
        # print(text)
        pass
    
    def on_logs(func):
        def redirect(self, txt):
            named_tuple = time.localtime() 
            time_string = time.strftime("%m-%d-%Y %H:%M:%S", named_tuple)
            
            data:dict = func(self, txt)
            text = (
                f"{data.get('color')}"
                f"[{time_string}][{data.get('service')}]: {data.get('text')}"
                f"{text_colors.RESET}"
            )
            
            self.callback(text)
            
            return text
        return redirect
    
    @on_logs
    def info(self, text):
        color = text_colors.GREY
        service = 'INFO'
        return {
            'text':text,
            'color':color,
            'service':service
        }
    
    @on_logs
    def warn(self, text):
        color = text_colors.YELLOW
        service = 'WARN'
        return {
            'text':text,
            'color':color,
            'service':service
        }
    
    @on_logs
    def error(self, text):
        color = text_colors.RED
        service = 'ERROR'
        return {
            'text':text,
            'color':color,
            'service':service
        }
    
    @on_logs
    def critical(self, text):
        color = text_colors.VIOLET
        service = 'CRITICAL'
        return {
            'text':text,
            'color':color,
            'service':service
        }
    
    @on_logs
    def success(self, text):
        color = text_colors.GREEN
        service = 'SUCCESS'
        return {
            'text':text,
            'color':color,
            'service':service
        }
    
    @on_logs
    def inportent(self, text):
        color = text_colors.BLUE
        service = 'IMPORTENT'
        return {
            'text':text,
            'color':color,
            'service':service
        }
    
    @on_logs
    def core(self, text):
        color = text_colors.CYAN
        service = 'CORE'
        return {
            'text':text,
            'color':color,
            'service':service
        }