

This is the API_Pharm project. This guide will help you set up your development environment and start the Django server.

## Prerequisites

- Python 3.x installed on your system
- Git installed on your system

## Setup Instructions

### Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/CodeNinja0852/API_Pharm.git
cd API_Pharm
Create a virtual environment
Next, create a virtual environment named env. Use the appropriate command based on your operating system:

For Windows
bash
Copy code
python -m venv env
.\env\Scripts\activate
For macOS and Linux
bash
Copy code
python3 -m venv env
source env/bin/activate
Install dependencies
Once the virtual environment is activated, install the required Python packages using pip:

bash
Copy code
pip install -r requirements.txt
Navigate to the main folder
Navigate to the main project folder api:

bash
Copy code
cd api
Apply migrations
Apply migrations to set up the database:

bash
Copy code
python manage.py migrate
Start the Django development server
Finally, start the Django development server:

bash
Copy code
python manage.py runserver
The development server will start running locally at http://127.0.0.1:8000/.

Additional Commands
Creating a new Django app
To create a new Django app within your project:

bash
Copy code
python manage.py startapp <app_name>
Creating a new superuser
To create a new superuser for the Django admin interface:

bash
Copy code
python manage.py createsuperuser
Running tests
To run tests for your Django project:

bash
Copy code
python manage.py test
Deactivating the Virtual Environment
To deactivate the virtual environment when you're done working on the project:

bash
Copy code
deactivate
Troubleshooting
If you encounter any issues during setup, please check the following:

Ensure Python and Git are properly installed and added to your system's PATH.
Make sure you have activated the virtual environment before installing dependencies or running the server.
Check for any errors in the terminal and follow the instructions provided to resolve them.
For further assistance, please refer to the official Django documentation or contact the project maintainer.

Happy coding!
# API
# API
# API
