from front.gui.main_window import WSEOapp
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

appName = config['ROOT']['APP_NAME']
version = config['ROOT']['VERSION']


