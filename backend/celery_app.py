from celery import Celery
from celery.schedules import crontab

from app import create_app


# ---------------- Flask App ----------------

flask_app = create_app()


# ---------------- Celery Factory ----------------

def make_celery(app):

    celery = Celery(

        app.import_name,

        broker=app.config["REDIS_URL"],

        backend=app.config["REDIS_URL"]

    )

    celery.conf.update(app.config)

    # ---------------- Timezone ----------------

    celery.conf.timezone = "Asia/Kolkata"

    celery.conf.enable_utc = False

    # ---------------- Beat Schedule ----------------

    celery.conf.beat_schedule = {

        # Daily Reminder (Every day at 8:00 AM)

        "daily-trek-reminder": {

            "task": "tasks.daily_trek_reminder",

            "schedule": crontab(

                hour=8,

                minute=0

            )

        },


        "monthly-admin-report": {

            "task": "tasks.monthly_admin_report",

            "schedule": crontab(

                day_of_month=1,

                hour=9,

                minute=0

            )
 

        },

        "auto-cancel-pending-bookings": {

            "task": "tasks.auto_cancel_pending_bookings",

            "schedule": 300.0

        },

    }

    # ---------------- Flask Context ----------------

    class ContextTask(celery.Task):

        def __call__(self, *args, **kwargs):

            with app.app_context():

                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


# ---------------- Celery Object ----------------

celery = make_celery(flask_app)


# ---------------- Import Tasks ----------------

import tasks