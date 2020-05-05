from __future__ import print_function
from collections import defaultdict, Counter
import os
import logging
import sys
from logging.handlers import RotatingFileHandler
import datetime
import configparser
import json

class Singleton(object):
    """
    Singleton interface:
    http://www.python.org/download/releases/2.2.3/descrintro/#__new__
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass

class LoggerManager(Singleton):
    """
    Logger Manager.
    Handles all logging files.
    """
    def init(self, loggername='root', debug=True, stdout=True):
        self.logger = logging.getLogger(loggername)
        rhandler = None
        FILENAME = 'logs/%s_%s.log'%(loggername,datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        LOG_FILENAME = os.path.join(os.getcwd(), FILENAME)
        formatter = logging.Formatter(
            fmt = '[%(asctime)s][%(filename)s:%(lineno)d][%(funcName)s][%(threadName)s][%(levelname)s]::%(message)s',
            datefmt = '%F %H:%M:%S'
        )

        try:
            rhandler = RotatingFileHandler(
                    LOG_FILENAME,
                    mode='a',
                    maxBytes = 10 * 1024 * 1024,
                    backupCount=5
                )
            if stdout:
               stdout_handler = logging.StreamHandler(sys.stdout)
               stdout_handler.setFormatter(formatter)
               self.logger.addHandler(stdout_handler)
        except:
            print(IOError("Couldn't create/open file \"" + \
                          LOG_FILENAME + "\". Check permissions."))
            rhandler = logging.StreamHandler(sys.stdout)

        if debug:
            self.logger.setLevel(logging.DEBUG)

        rhandler.setFormatter(formatter)
        self.logger.addHandler(rhandler)

    def debug(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.debug(msg)

    def error(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.error(msg)

    def info(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.info(msg)

    def warning(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.warning(msg)

    def set(self, loggername):
        self.logger = logging.getLogger(loggername)
        


class Logger(object):
    """
    Logger object.
    """
    def __init__(self, loggername="root", debug=True, stdout=True):
        self.lm = LoggerManager(loggername, debug) # LoggerManager instance
        self.loggername = loggername # logger name

    @property
    def logger(self):
        return self.lm.logger

    @property
    def debug(self):
       self.lm.set(self.loggername)
       return self.logger.debug

    @property
    def info(self):
       self.lm.set(self.loggername)
       return self.logger.info

    @property
    def error(self):
       self.lm.set(self.loggername)
       return self.logger.error

    @property
    def warning(self):
       self.lm.set(self.loggername)
       return self.logger.warning
      


class TimeInspector(Singleton):
    __metaclass__ = Singleton
    counter = 0
    _distinct = None
    
    @staticmethod
    def get_instance():
        if TimeInspector._distinct is None:
            ojb = TimeInspector()
            TimeInspector._distinct = ojb
        return TimeInspector._distinct
        
    def __init__(self):
        self.data = {}
        #TimeInspector.counter += 1
    
    def get_name(self, func):
        #print(repr(func), repr(func).split(" "))
        string = repr(func).split(" ")[1]
        return string
    
    
    def __repr__(self):
        return '<%s.%s object at %s>\n%s' % (
        self.__class__.__module__,
        self.__class__.__name__,
        hex(id(self)),
    '\n'.join([repr(item) for item in self.data.items()]))
    
#     @classmethod
#     def get_name(cls, func):
#         string = repr(func).split(" ")[1]
    
#     @classmethod
#     def get_info(cls):
#         print(cls.data)
    
    def init_dict(self):
        return {'count':0, 'total_time': 0, 'avg_time': 0, 'avg_perloop': 0}
    
    def __call__(self, func):
        def decorator(*args, **kwargs):
            func_name = self.get_name(func)
            data_dict = self.data.get(func_name, self.init_dict())
            #print('unknow check',func_name, self, self.counter)
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            data_dict['count'] += 1
            data_dict['total_time'] += duration
            data_dict['avg_time'] = '%.8f s'%(data_dict['total_time']/data_dict['count'])
            data_dict['avg_perloop'] = data_dict['total_time']/1000
            self.data[func_name] = data_dict
            return result
        return decorator

class Configuration(Singleton):
    def __init__(self, filepath=None, **kwargs):
        self._configs = {}
        self.filepath = filepath
        self.reset(**kwargs)

    def reset(self, **kwargs):
        if self.filepath is None:
            self._configs = kwargs
        else:
            assert os.path.exist(filepath),IOError('% not exist, please check '%filepath)
            config = configparser.ConfigParser()
            config.read(filepath)
            the_dict = {}
            for section in config.sections():
                the_dict[section] = {}
                for key, val in config.items(section):
                    the_dict[section][key] = val
            self._configs = the_dict

    def update(self, data):
        self._configs.update(data)

    def __repr__(self):
        data = json.dumps(self._configs, indent=4)
        return data

    def __getitem__(self,index):
        return self._configs[index]

    def __setitem__(self, index, value):
        self._configs[index] = value

    @property
    def configs(self):
        return self._configs         
           


def test():
    logger = Logger()
    logger.info('Running test...')
    timecounters = [TimeInspector().__hash__, TimeInspector().__hash__]
    loggers = [Logger(), Logger()]
    loggers[0].debug(repr(loggers))
    loggers[1].debug(repr(loggers))
    logger.debug(repr((timecounters, loggers)))

if __name__ == '__main__':

    #unittest.main()
    test()
