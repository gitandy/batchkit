import sys
import time
import subprocess

__author__ = 'Andreas Schawo <andreas@schawo.de>, (c) 2021'
__license__ = 'This work is licensed under CC BY 4.0 https://creativecommons.org/licenses/by/4.0/'
__version__ = 'v0.1'


class BatchKit:
    def __init__(self):
        self.last_error = None

    def get_err(self):
        """:return The last error text"""
        err = self.last_error
        self.last_error = None
        return err

    @staticmethod
    def get_date():
        """Returns The current date in format yyyy-mm-dd"""
        return time.strftime('%Y-%m-%d')

    @staticmethod
    def get_time():
        """:return The current time in format HH:MM:SS"""
        return time.strftime('%H:%M:%S')

    def txt_write(self, txt, file):
        """Writes text to a file to substitute '>'
        :return True if everything went well, false otherwise"""
        try:
            with open(file, 'wt') as f:
                f.write(txt)
            return True
        except OSError as e:
            self.last_error = str(e)
            return False

    def txt_append(self, txt, file):
        """Writes text to a file to substitute '>>'
        :return True if everything went well, false otherwise"""
        try:
            with open(file, 'at') as f:
                f.write(txt)
                return True
        except OSError as e:
            self.last_error = str(e)
            return False

    def txt_read(self, file):
        """Reads text from a file to substitute '<'
        :return Text if everything went well, None otherwise"""
        try:
            with open(file, 'rt') as f:
                txt = f.read()
            return txt
        except OSError as e:
            self.last_error = str(e)
            return None

    def run_proc(self, *proc):
        """Runs a process with arguments
        :return Tuple of return code, stdout text, stderr text"""
        try:
            res = subprocess.run(list(proc) if type(proc) is tuple else [proc], capture_output=True)
            return {'returncode': res.returncode, 
                    'stdout': str(res.stdout, sys.getdefaultencoding()).replace('\r', ''), 
                    'stderr': str(res.stderr, sys.getdefaultencoding().replace('\r', ''))}
        except OSError as e:
            self.last_error = str(e)
            return None

    @staticmethod
    def get_name():
        """:return The path of the script (which imports Batch-Kit)"""
        if hasattr(sys.modules['__main__'], '__file__'):
            return sys.modules['__main__'].__file__
        else:
            return ''

    @staticmethod
    def get_ver():
        """:return The version of Batch-Kit"""
        return __version__
