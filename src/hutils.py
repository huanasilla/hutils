from __future__ import print_function
from collections import defaultdict, Counter
import os
import logging
import sys
from logging.handlers import RotatingFileHandler
import datetime
import configparser
import json
import time
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
    def init(self, loggername='root', **kwargs):
        self.kwargs = kwargs
        self.loggername = loggername
        #print('Initialize logger', loggername, kwargs)
        self.logger = logging.getLogger(loggername)
        rhandler = None
        LOG_FILENAME = kwargs.get('filename', None)
        if LOG_FILENAME is None:
           FILENAME = 'logs/%s_%s.log'%(loggername,datetime.datetime.now().strftime("%Y%m%d_%H"))
           LOG_FILENAME = os.path.join(os.getcwd(), FILENAME)
        formatter = kwargs.get('formatter', None)
        
        if formatter is None:
           formatter = logging.Formatter(
               fmt = '[%(asctime)s][%(filename)s:%(lineno)d][%(funcName)s][%(threadName)s][%(levelname)s]::%(message)s',
               datefmt = '%F %H:%M:%S'
           )

        debug = kwargs.get('debug', True)
        stdout = kwargs.get('stdout', True)
        
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
        self.logger.info('Start logging into : %s'%LOG_FILENAME)
        self.logger.propagate = False

    def debug(self, loggername, msg):
        #self.logger = logging.getLogger(loggername)
        self.logger.debug(msg)

    def error(self, loggername, msg):
        #self.logger = logging.getLogger(loggername)
        self.logger.error(msg)

    def info(self, loggername, msg):
        #self.logger = logging.getLogger(loggername)
        self.logger.info(msg)

    def warning(self, loggername, msg):
        #self.logger = logging.getLogger(loggername)
        self.logger.warning(msg)

        


class Logger(object):
    """
    Logger object.
    """
    def __init__(self, loggername="root", **kwargs):
        self.lm = LoggerManager(loggername,  **kwargs) # LoggerManager instance
        self.loggername = loggername # logger name
        self.kwargs = kwargs
        self.info('Link logger "%s" into "%s"'%(self.loggername, self.lm.loggername))
    
    @property
    def logger(self):
        return self.lm.logger

    @property
    def debug(self):
       return self.logger.debug

    @property
    def info(self):
        return self.logger.info

    @property
    def error(self):
       return self.logger.error

    @property
    def warning(self):
       return self.logger.warning
      


class TimeInspector(Singleton):
    counter = 0

    def __init__(self, threshold=0.005, skip=False):
        self.data = {}
        self._skip = skip
        self.threshold = threshold
        #TimeInspector.counter += 1

    def set_skip(self):
        'ignore cal time'
        self._skip = True
        
    def get_name(self, func):
        #print(repr(func), repr(func).split(" "))
        string = repr(func).split(" ")[1]
        return string
    
    
    def __repr__(self):
        data = {}
        for item in self.data.items():
            key, val = item
            if float(val['avg_time'].split('s')[0]) > self.threshold:
               data[key] = val
        data = json.dumps(self.data, indent=2)
            
        return '<%s.%s object at %s>\n%s' % (
        self.__class__.__module__,
        self.__class__.__name__,
        hex(id(self)),
        data)
    
    def init_dict(self):
        return {'count':0, 'total_time': 0, 'avg_time': 0}
    
    def __call__(self, func):
        if self._skip:
           return func
 
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
            #data_dict['avg_perloop'] = data_dict['total_time']/1000
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
