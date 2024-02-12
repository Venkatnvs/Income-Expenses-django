set -o errexit
echo "Build Start"

python -m pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py makemigrations
python manage.py migrate
# python manage.py createsuperuser --noinput --email=venkatnvs2005@gmail.com

echo "End Build"