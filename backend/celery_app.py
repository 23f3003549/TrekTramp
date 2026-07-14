from celery import Celery
from app import create_app

flask_app = create_app()


def make_celery(app):

    celery = Celery(
        app.import_name,
        broker=app.config["REDIS_URL"],
        backend=app.config["REDIS_URL"]
    )

    celery.conf.update(app.config)

    class ContextTask(celery.Task):

        def __call__(self, *args, **kwargs):

            with app.app_context():

                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(flask_app)

# Import tasks so Celery can discover them
import tasks