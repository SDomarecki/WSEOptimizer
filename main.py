# inactve - see backend/genetic/GA_main.py
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

appName = config['ROOT']['APP_NAME']
version = config['ROOT']['VERSION']


