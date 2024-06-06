# some useful commands to run the backend
docker run -d --name broker redis
celery -A pro worker --loglevel=DEBUG --concurrency=4 -P eventlet -n worker1
celery -A pro worker --loglevel=DEBUG --concurrency=4 -P eventlet -n worker2
celery -A pro status

python3 manage.py runserver 

# 
docker run --name postgres -e POSTGRES_PASSWORD=rasta -d postgres
docker exec -it some-postgres psql -U postgres

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'


docker compose up airflow-init

# some timescale commands
psql "postgres://tsdbadmin:nt9c9ffcdgr2c6vh@fmsrxhtln8.y7n8z210d2.tsdb.cloud.timescale.com:33078/tsdb?sslmode=require"