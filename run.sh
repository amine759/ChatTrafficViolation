# some useful commands to run the backend
docker run -d --name broker redis
sleep 1
celery -A pro worker --loglevel=DEBUG --concurrency=4 -P eventlet -n worker1
celery -A pro worker --loglevel=DEBUG --concurrency=4 -P eventlet -n worker2
celery -A pro status
sleep 1
python3 manage.py runserver 

# 
docker run --name some-postgres -e POSTGRES_PASSWORD=rasta -d postgres