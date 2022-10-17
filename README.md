## PLEASE USE PYTHON 3.7 FOR SETUP

<ol>
    <li>Create a virtualenv and activate it.(optional)</li> 
    <li>cd to project folder</li> 
    <li>Install the requirements using "pip install -r requirements.txt"</li>
    <li>Create MySql database</li>
    <li>Create .env file in project folder(scholarship_mgmt) and set the value of following variables. (see .env_sample file)
        <ul>
            <li>SECRET_KEY=<your_django_secret_key></li>
            <li>DATABASE_NAME=your_db_name</li>
            <li>DATABASE_USER=database_user_name</li>
            <li>DATABASE_USER=database_user_name</li>
            <li>DATABASE_PASS=<database_password></li>
            <li>BASE_API_URL=http://127.0.0.1:port</li>
        </ul>
    </li>

<li>Add the database credentials in settings.py. e.g<br/>
    DATABASES = {<br/>
        'default': {<br/>
            'ENGINE': 'django.db.backends.postgresql_psycopg2',<br/>
            'NAME': env('DATABASE_NAME'),<br/>
            'USER': env('DATABASE_USER'),<br/>
            'PASSWORD': env('DATABASE_PASS'),<br/>
            'HOST': 'localhost',<br/>
            'PORT': '5432',<br/>
        }<br/>
    }<br/>
</li>
    <li>After connecting the database apply the migrations using "python manage.py migrate" command</li>
    <li>Last step run the server using "python manage.py runserver" command and access the admin panel at http://127.0.0.1:8000/admin.</li>
</ol>