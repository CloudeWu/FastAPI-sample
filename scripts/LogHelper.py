import os

class LogHelper():
    LOG_LEVELS = ['ERROR', 'WARN', 'INFO', 'DEBUG']
    def __init__(self, log_level=2, log_file=None, no_print=False):
        self.current_log_level = log_level
        self.no_print = no_print
        if log_file:
            self.ensure_path_exist(log_file)
            self.logger = open(log_file, 'w+', encoding='utf-8')
        else:
            self.logger = None

    def log(self, type, message):
        """ Print and write log message with format " [ {TYPE} ] {MESSAGE}\n" if log type > log level
        @param type -- type of log message. ['ERROR', 'WARN', 'INFO', 'DEBUG']
        """
        log_level, log_tag = self.get_log_level(type)
        if self.current_log_level < log_level:
            return
        
        if not self.no_print:
            print(f' [ {log_tag} ] {message}')

        if self.logger:
            self.logger.write(f' [ {type.upper()} ] {message}\n')

    def get_log_level(self, type):
        """ Transform log type into log level and tags
        @ret (log_level, log_tag)
        """
        log_tag = type.upper()
        try:
            log_level = self.LOG_LEVELS.index(type.upper())
        except ValueError:
            # treat all other tags as INFO
            log_level = 2
        return log_level, log_tag

    def __del__(self):
        if self.logger:
            self.logger.close()
    
    @staticmethod
    def ensure_path_exist(filename):
        """
        Ensure all folders on file's path exist
        """
        file_dir = os.path.dirname(filename)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            print(f' [ INFO ] folder {file_dir} created')