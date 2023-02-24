from bot import application
import sys
import logging
import services
from nsmu_parser import get_groups, get_specs

from bot.handlers.subscribers import *
from bot.handlers.common import *
from bot import application

logging.basicConfig(level=logging.INFO)


def get_groups_and_specializations():
    for spec in get_specs():
        last_spce = services.create_spec(spec.title, spec.href)
        for group in get_groups(spec.href):
            services.create_group(group.title, group.href,
                                  last_spce.specialization_id)


if __name__ == "__main__":
    args = sys.argv

    command = args[1]

    if command == 'run':
        logging.info('Runing bot...')
        application.run_polling()

    if command == 'init':
        logging.info('Init db...')
        get_groups_and_specializations()
