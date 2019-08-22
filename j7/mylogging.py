
import logging

logger=logging.getLogger("j7")
f_handler = logging.FileHandler('j7/log/app.log',mode='w')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)