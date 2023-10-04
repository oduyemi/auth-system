from celery import Celery
from authsys_app import app

celery = Celery('authsys_app', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

if __name__ == '__main__':
    celery.worker_main(['worker', '--loglevel=info', '-A', 'authsys_app.celery'])
