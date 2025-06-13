## install
pip install git+https://github.com/assem-ch/django-jet-reboot
pip install -r requirements.txt

## Run
```
python manage.py collectstatic
python manage.py migrate
python manage.py createcachetable
python manage.py runserver
```