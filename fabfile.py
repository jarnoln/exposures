# Very simple deploy script using Fabric 2.x
from fabric import task

@task
def deploy(c):
    source_directory = '/home/{}/sites/exposures/source'.format(c.user)
    c.run('cd {} && git pull'.format(source_directory))
    c.run('. {}/reset-gunicorn.sh'.format(source_directory))
