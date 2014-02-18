#-*- coding: utf-8 -*-
try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError

from nose import plugins, config

from selenose.server import Server
from selenose.configs import ServerConfig, DriverConfig

class GlobalDriverEnv(object):
    environment = None

    @classmethod
    def set_env(cls, env):
        cls.environment = env

    def get_driver(self):
        return self.environment.create()


def all_config_files(options, conf):
    '''
    Get the list of configuration files.
    '''
    # Get default configuration files
    files = config.all_config_files()
    # Get the files from configuration
    files.extend(getattr(conf, 'files', []))
    # Check if options has files
    if getattr(options, 'files', []):
        # Get files from options
        files.extend(options.files)
    # Return the full list
    return files

class SeleniumServerPlugin(plugins.Plugin):
    '''Start a Selenium server before running tests.'''
    
    name = 'selenium-server'

    def configure(self, options, conf):
        '''
        Configure the plug-in.
        '''
        # Call super
        super(SeleniumServerPlugin, self).configure(options, conf)
        # Initialize the server
        self.server = Server(ServerConfig(all_config_files(options, conf)))

    def begin(self):
        '''
        Start the SELENIUM server.
        '''
        self.server.start()
    
    def finalize(self, result):
        '''
        Stop the SELENIUM server.
        '''
        self.server.stop()

class SeleniumDriverPlugin(plugins.Plugin):
    '''Provide a WebDriver to the tests.'''
    
    name = 'selenium-driver'

    def options(self, parser, env):
        '''
        Add plug-in options.
        '''
        # Call super
        super(SeleniumDriverPlugin, self).options(parser, env)
        # Add environment input
        parser.add_option('--selenium-driver', action='store', dest='env', help='Enable the provided environment.')

    def configure(self, options, conf):
        '''
        Configure the plug-in.
        '''
        # Call super
        super(SeleniumDriverPlugin, self).configure(options, conf)
        # Check if enabled
        if self.enabled:
            # Check if an environment is provided
            if not options.env:
                # Not provided, raise
                raise ValueError('please provide a driver environment')
            # Get the environment
            GlobalDriverEnv.set_env(DriverConfig(all_config_files(options, conf)).getenv(options.env))
