# Very simple deploy script using Fabric 2.x
import datetime

from fabric import task

@task
def deploy(c):
    source_directory = '/home/{}/sites/exposures/source'.format(c.user)
    c.run('cd {} && git pull'.format(source_directory))
    c.run('. {}/deploy/reset-gunicorn.sh'.format(source_directory))

@task
def backup(c):
    db_file_path = '/home/{}/sites/exposures/source/db.sqlite3'.format(c.user)
    now = datetime.datetime.now()
    local_name = now.strftime('%Y-%m-%d_%H_%M_db.sqlite3')
    print(local_name)
    result = c.get(db_file_path, local=local_name)
    print('Copied {} from {} to {}'.format(db_file_path, result.remote, result.local))
