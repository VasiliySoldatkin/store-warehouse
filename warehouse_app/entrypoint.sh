set -e;
if [[ ! $APP_HOST ]]
then
  APP_HOST=0.0.0.0
fi
if [[ ! $APP_PORT ]]
then
  APP_PORT=8000
fi
./manage.py makemigrations && ./manage.py migrate
python3 ./manage.py runserver $APP_HOST:$APP_PORT
exec "$@"
