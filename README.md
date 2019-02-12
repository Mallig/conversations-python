## Conversation API - Python

This is a remake of an API originally created in Ruby. It's not too complex so thought it would be a good opportunity to learn some Python.
The purpose of this API is to provide a clone of WhatsApp with groups of messages between users. These messages will be displayed through a frontend built using React. At the moment there are two different groups of messages the API needs to be able to return, all messages between two users and a users most recent message for each of their conversations.

This project is using Flask, Postgresql with SQLAlchemy.

## Running the API

Python can be installed with

`~ brew install python`

This will also install pip - the python package installer, and venv - environment manager for python projects.

If create a virtual environment in which to manage app dependencies, `cd` to the project directory and run

`~ python3 -m venv <venv_name>`

This will create a directory on the project root by the name you choose, containing a key pointing to the Python installation used in the command along with scripts (in bin/) and site packages.

To enter the virtual environment run

`~ source <venv_name>/bin/activate` 
 
(run `~ deactivate` to exit venv)

To install the dependencies to a virtual environment just for this project run 

`~ pip install -r requirements.txt`

Nearly there, all you need to do now is tell Flask where to find the application and the environment, run

```shell
~ export FLASK_APP=api
~ export FLASK_ENV=development
```

And you're done! Run the application with 

`flask run`

Easy peasy.

## Running Tests

Tests are written using pytest with help from pytest-flask, and coverage from pytest-cov. Make sure the virtual environment has been activated then run the tests with:

`python -m pytest --cov=api test/`

add the flag `-v` or `-vv` from more detail

Tests achieve 100% coverage through integration tests, 74% through unit tests as the conversation controller is not yet tested.
