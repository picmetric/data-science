import logging
from logging.handlers import RotatingFileHandler
from os import path

LOGFILE = path.join(
	path.dirname(
		path.abspath(__file__)
	), 'logs/flask.log'
)


def startLog(file):
	log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(funcName)s(%(lineno)d) %(message)s')

	if file is not None:
		my_handler = RotatingFileHandler(file, mode='a', maxBytes=1 * 1024 * 1024,
									backupCount=10, encoding=None, delay=0)
	else:
		my_handler = logging.StreamHandler()
	my_handler.setFormatter(log_formatter)
	my_handler.setLevel(logging.DEBUG)

	app_log = logging.getLogger('root')
	app_log.setLevel(logging.DEBUG)

	app_log.addHandler(my_handler)
	app_log.critical('********************************')
	app_log.critical('App started, logging initialized')
	return(app_log)

