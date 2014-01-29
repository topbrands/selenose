#-*- coding: utf-8 -*-
import unittest

class SeleniumTestCase(unittest.TestCase):
    '''
    SELENIUM test case.
    '''
    # Flag to notify that it is a SELENIUM test
    enable_selenium_driver = True

    def setUp(self):
        super(SeleniumTestCase, self).setUp()
        self.driver = self.driver_env.create() #create driver from injected environment

    def tearDown(self):
        super(SeleniumTestCase, self).tearDown()
        # If quit already called in test, produces a URLError, so catch it
        try:
            # Quit
            self.driver.quit()
        # Ignore error if quit already
        except URLError:
            pass


try:
    import django.test
except ImportError, e: pass
else:
    try:
        from urllib.error import URLError
    except ImportError:
        from urllib2 import URLError
    import selenose.tasks.selenium_driver

    class LiveServerTestCase(django.test.LiveServerTestCase):
        '''
        SELENIUM test case for DJANGO.
        '''
    
        @classmethod
        def setUpClass(cls):
            # Get the environment
            env = selenose.tasks.selenium_driver.env
            # Check if defined
            if env is None:
                # If not raise an exception
                raise ValueError('please set the environment')
            # Create the driver
            cls.driver = selenose.tasks.selenium_driver.env.create()
            # Call super
            super(LiveServerTestCase, cls).setUpClass()
    
        @classmethod
        def tearDownClass(cls):
            # Call super
            super(LiveServerTestCase, cls).tearDownClass()
            # If quit already called in test, produces a URLError, so catch it
            try:
                # Quit
                cls.driver.quit()
            # Ignore error if quit already
            except URLError: pass
            # Reset
            cls.driver = None
