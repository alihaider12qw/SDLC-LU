import logging
import sys

from .registry import schedules_registry, tasks_registry

formatter = logging.Formatter(
    "[%(asctime)s %(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger = logging.getLogger("scheduler")
logger.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(file_handler)


def show_registry():
    """Helper functions that shows the registry contents"""

    if len(schedules_registry):
        schedules_names = ", ".join(schedules_registry.keys())
        logger.info(
            f"{len(schedules_registry)} schedules registered: {schedules_names}"
        )
    else:
        logger.info("No schedules registered")

    if len(tasks_registry):
        tasks_names = ", ".join(tasks_registry.keys())
        logger.info(f"{len(tasks_registry)} tasks registered: {tasks_names}")
    else:
        logger.info("No tasks registered")
