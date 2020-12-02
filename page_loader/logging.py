import logging
import logging.config

config = {
    'version': 1,
    'formatters': {
        'time_level_msg': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'time_level_msg',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['stderr'],
        },
    },
}

logging.config.dictConfig(config)
logger = logging.getLogger('root')
