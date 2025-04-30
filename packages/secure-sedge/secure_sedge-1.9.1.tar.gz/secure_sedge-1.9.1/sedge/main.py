from logging.config import dictConfig
from raft import Collection, Program
from . import cert_tasks
from . import installers


dictConfig(dict(
    version=1,
    formatters=dict(
        timed={
            '()': 'colorlog.ColoredFormatter',
            'format': '{log_color}[{asctime}.{msecs:03.0f}] {message}',
            'datefmt': '%H:%M:%S',
            'style': '{',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'fg_bold_red',
            }
        }
    ),
    handlers={
        'console-brief': {
            'class': 'logging.StreamHandler',
            'formatter': 'timed',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        }
    },
    root=dict(
        handlers=[ 'console-brief', ],
        level='INFO',
    ),
    loggers={
        'sedge': {
            'level': 'INFO',
            'handlers': [ 'console-brief', ],
            'propagate': False,
        }
    }
))
ns = Collection.from_module(cert_tasks)
ns.add_collection(installers.installers_collection, 'install')
program = Program(version='1.9.1', namespace=ns)
