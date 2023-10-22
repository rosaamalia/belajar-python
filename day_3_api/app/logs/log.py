import logging

logging.basicConfig(filename=r'D:\Belajar\belajar-python\day_3_api\app\logs\log_flask.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('test_logger')