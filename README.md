PharmaNexus
=========

Chembid is a web based application that helps users to buy raw materials and sell products, non-moving stock from a huge database of pharmaceutical and chemical companies. Basically this project contains a Back-end database which is linked to the homepage's search bar. 



## Running the project  

#### Install Python

First of all check if python is installed on your device. To check if you have it installed (and which version it is), type the following command:

```python3 --version```

If you don't have Python installed, or if you want a different version, you can install it as follows:

```sudo apt-get install python3.5```

#### Set up virtualenv

Virtual environment can be created by the following command:

```virtualenv -p /usr/bin/python3 <name of your virtualenv>```

#### Running the project

At first activate the virtual environment created by the following command:

```source <name of your virtualenv>/bin/activate```

* To install all the requirements for running the project, type the following command:

  ```pip install -r requirements.txt```

* to In SSAD39/src/mysite/mysql.cnf,  write your own mysql credentials.

* Then create a database named chembid in your mysql.

* In SSAD39/src/mysite/settings.py, write the path of your mysql.cnf file in DATABASES object.

* Now go into the src directory and run the following commands to migrate database:

  ```python manage.py makemigrations```

  ```python manage.py migrate```

* Now to run the server type the following command:

  ```python manage.py runserver```

* No go to your localhost (127.0.0.1) in web browser.

## Features

1. User can search for various items using home's search bar.
2. Authentication (Sign Up) is required for using the site.
3. There is an admin dashboard through which admin can perform CRUD operations.
4. Database can be changed by admin. Admin can directly load .xls files to add it in database.
5. Authenticated users can also upload the details of products (max. 5) which they want to sell.

