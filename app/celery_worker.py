from celery import Celery

celery = None

def make_celery(app):
    global celery
    celery = Celery(
        app.import_name,
        broker=app.config.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),
        backend='rpc://'  # Αντί για Redis backend, χρησιμοποιεί RPC
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
