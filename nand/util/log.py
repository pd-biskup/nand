import nand.util.config as config


class Logger:

    def __init__(self, output=config.log_output, color=config.color):
        self.output = output
        self.color = color
    
    def log(self, message, level):
        if config.log_level >= level:
            msg = '['
            if config.color:
                if level == config.Level.ERR:
                    msg += config.colors['red']
                elif level == config.Level.WRN:
                    msg += config.colors['yellow']
                elif level == config.Level.DBG:
                    msg += config.colors['green']
                msg += level.name + config.colors['default']
            else:
                msg += level.name
            msg += '] ' + message + '\n'
            for out in self.output:
                out.write(msg)
            

log = Logger()
