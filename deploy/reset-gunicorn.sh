PID=$(systemctl show --value -p MainPID gunicorn.service) && kill -HUP $PID

