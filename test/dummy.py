from hutils import *
import unittest

class Testing(unittest.TestCase):
    
    def test_config(self):
        filename = '__testconfig__.ini'
        config = Configuration()
        data = {'First Section': {'var': 'value', '__name__': 'First Section', 'key': 'item'},
                'Second Section': {'__name__': 'Second Section', 'otherkey': 'otheritem', 'othervar': 'othervalue'}}
        config.update(data)
        self.assertEqual(config['First Section'], {'var': 'value', '__name__': 'First Section', 'key': 'item'})
        
        config_parser = configparser.ConfigParser()
        config_parser.read_dict(config.configs)
        with open(filename, 'w') as configfile:
             config_parser.write(configfile)
        config_test = Configuration(filename=filename)
        print(os.path.abspath(filename),'\n', repr(config))
        self.assertEqual(config_test.configs, config.configs)
        os.remove(filename)
        
        
        
    def test_timeinspector(self):
        caltime1 = TimeInspector()
        caltime2 = TimeInspector()
        self.assertEqual(hex(id(caltime1)), hex(id(caltime2)))
    
    def test_logger(self):
        logger = Logger()
        timecounters = [TimeInspector(), TimeInspector()]
        loggers = [Logger(), Logger()]
        loggers[0].debug(loggers)
        loggers[1].debug(loggers)
        logger.debug(timecounters)
        self.assertEqual(logger.lm, loggers[0].lm)
        
        #unittest.main()


    def test_string(self):
        a = 'some'
        b = 'some'
        self.assertEqual(a, b)

    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)
        
def suite():
    return unittest.makeSuite(Testing)

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
    
