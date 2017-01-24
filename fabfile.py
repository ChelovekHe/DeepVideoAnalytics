import os,logging
from fabric.state import env
from fabric.api import task,local,run,put,get,lcd,cd,sudo
import django,sys
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')


@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()


@task
def shell():
    local('python manage.py shell')


@task
def make_migrate():
    local('python manage.py makemigrations')


@task
def local_static():
    local('python manage.py collectstatic')


@task
def migrate():
    local('run python manage.py migrate')


def setup_django():
    os.environ["DJANGO_SETTINGS_MODULE"] = "dva.settings"
    django.setup()

@task
def worker(queue_name,conc=1):
    conc = int(conc)
    command = 'celery -A dca worker -l info -c {} -Q {} -n {}.%h -f logs/celery.log'.format(conc,queue_name,queue_name)
    if sys.platform != 'darwin':
        command = "source ~/.profile && "+command
    local(command=command)


@task
def server():
    local('python manage.py runserver')

@task
def rmq():
    local('python manage.py runserver')

# @task
# def setup_test(sure,local_test=False):
#     if sure == 'yes':
#         setup_django()
#         from dva_app.models import Video,Frame,Detection
#         from dva_app.tasks import extract_frames,Q_EXTRACTOR
#         Detection.objects.all().delete()
#         Frame.objects.all().delete()
#         Video.objects.all().delete()
#         for k in range(1,20):
#             v = Video()
#             v.key = "videos/1{}.mp4".format(k)
#             v.bucket = "aub3dca"
#             v.length_in_seconds = 0
#             v.frames = 0
#             v.save()
#             if (not local_test) or k == 1:
#                 extract_frames.apply_async(args=[v.id,], queue=Q_EXTRACTOR)
#
#
# @task
# def test():
#     setup_django()
#     from dca_app.models import Video
#     from dca_app.tasks import perform_indexing,Q_INDEXER
#     for v in Video.objects.all.filter(key="videos/1.mp4"):
#         perform_indexing.apply_async(args=[v.id,], queue=Q_INDEXER)