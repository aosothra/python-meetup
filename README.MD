# Python-Meetup

This project implements a Telegram bot application for management of public events (expos, conventions, etc)

Following functions are implemented through Telegram Bot:
- Traverse of event schedule by attendees
- Networking system, where attendees can register and match with other applicants for personal contact
- Q&A system, where attendees can direct questions to speakers, and speakers can filter and answer those questions
- Donations

Following functions are implemented through admin interface:
- Creation of events with different flows, blocks and presentations
- Notification broadcast to all attendees in Telegram
- Gathering, display and export of simple analytic data about received donations

## Setup in development

This project is made in Python 3, so make sure that you have Python and pip installed on your system.

It is recommended to use `venv`/`virtualenv` for environment isolation. You can set up and activate your virtual environment with these commands:
```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install required dependencies using following command:
```sh
pip install -r requirements.txt
```


Create `.env` file in the root directory of your repository. This file will be used to load environment variables, some of which are mandatory for proper execution. You can refer to `.env.example` for quick setup, or follow bullet points below:
- `SECRET_KEY` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value. [(Django doc)](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key)
- `TG_BOT_TOKEN` - Telegram Bot access token, provided by @BotFather upon creation. [(Telegram Bot API)](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
- `PAYMENT_BOT_TOKEN` - Payment system token registered for your bot. [(Bot Payment API)](https://core.telegram.org/bots/payments)

Following setting are optional:
- `ALLOWED_HOSTS` - (DEFAULT: `127.0.0.1`) A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations. [(Django doc)](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts)
- `DEBUG` - (DEFAULT: `False`) A boolean that turns on/off debug mode. *Never deploy a site into production with DEBUG turned on.* [(Django doc)](https://docs.djangoproject.com/en/3.2/ref/settings/#debug)
- `DATABASE_URL` - (DEFAULT: `sqlite:///$PROJECT_ROOT/db.sqlite3`) - 12factor inspired URL to your database. [(dj-database-url)](https://pypi.org/project/dj-database-url/)

Once your `.env` is all set up, it is time to apply migrations to your development database:
```sh
python3 manage.py migrate
```

You can use following command to populate DB with testing data:
```sh
python3 manage.py create_fake_event
```
Testing data is loaded from `fake_event_map.json` in the root of your project.

You can start your Admin web app...
```sh
python3 manage.py runserver
```

...and your bot instance:
```sh
python3 manage.py runbot
```

## Setup in production

[Docker Compose](https://docs.docker.com/compose/) is used to deploy and run the project in production as multi-container Docker application. Make sure you have Docker and Docker Compose Plugin installed.

For details of containerization refer to `docker-compose.yml`.

PostgreSQL is used as database system. Create `.env.prod.db` file in the root of your project with following variables defined:
- `POSTGRES_DB` - alias of your database in production.
- `POSTGRES_USER` - username from which the database is accessed.
- `POSTGRES_PASSWORD`- password to access the database.

Then create `.env.prod` file in the root of your project with following variables defined:
- `SECRET_KEY` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value. [(Django doc)](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key)
- `TG_BOT_TOKEN` - Telegram Bot access token, provided by @BotFather upon creation. [(Telegram Bot API)](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
- `PAYMENT_BOT_TOKEN` - Payment system token registered for your bot. [(Bot Payment API)](https://core.telegram.org/bots/payments)
- `DATABASE_URL` - (DEFAULT: `sqlite:///$PROJECT_ROOT/db.sqlite3`) - Once in production, make sure to specify a proper `postgres` link in the following way: `postgres://USER:PASSWORD@db:5432/ALIAS` [(dj-database-url)](https://pypi.org/project/dj-database-url/)

Following setting are optional:
- `ALLOWED_HOSTS` - (DEFAULT: `127.0.0.1`) A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations. [(Django doc)](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts)
- `DEBUG` - (DEFAULT: `False`) A boolean that turns on/off debug mode. *Never deploy a site into production with DEBUG turned on.* [(Django doc)](https://docs.djangoproject.com/en/3.2/ref/settings/#debug)
  
At this point you can deploy your application using following command:
```sh
docker compose up -d --build
```
This will deploy 4 containers:
- `*_db` with your postgres database instance.
- `*_web` with Gunicorn instance running your Django app through WSGI
- `*_bot` with your bot instance (uses the same image as `*_web`)
- `*_nginx` with Nginx instance configured as reverse-proxy and for static files serving.

# Goal

This project was created as Team Work exercise on [Devman](https://dvmn.org/) Python Developer course.