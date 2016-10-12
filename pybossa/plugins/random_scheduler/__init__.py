import pybossa.sched as sched
from pybossa.forms.forms import TaskSchedulerForm
from pybossa.core import project_repo
from flask.ext.plugins import Plugin
from functools import wraps
import random

__plugin__ = "RandomScheduler"
__version__ = "0.0.1"

SCHEDULER_NAME = 'random'


def get_random_task(project_id, user_id=None, user_ip=None,
                    n_answers=30, offset=0):
    """Return a random task for the user."""
    project = project_repo.get(project_id)
    if project and len(project.tasks) > 0:
        return random.choice(project.tasks)
    else:
        return None


def with_random_scheduler(f):
    @wraps(f)
    def wrapper(project_id, sched, user_id=None, user_ip=None, offset=0):
        if sched == SCHEDULER_NAME:
            return get_random_task(project_id, user_id, user_ip, offset=offset)
        return f(project_id, sched, user_id=user_id, user_ip=user_ip, offset=offset)
    return wrapper


def variants_with_random_scheduler(f):
    @wraps(f)
    def wrapper():
        return f() + [(SCHEDULER_NAME, 'Random')]
    return wrapper


class RandomScheduler(Plugin):

    def setup(self):
        sched.new_task = with_random_scheduler(sched.new_task)
        sched.sched_variants = variants_with_random_scheduler(sched.sched_variants)
        TaskSchedulerForm.update_sched_options(sched.sched_variants())
