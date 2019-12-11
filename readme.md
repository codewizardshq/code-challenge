# Instructions for Flask

- Before begining please create a .flaskenv file with the following contents

```
FLASK_ENV="development"
FLASK_APP="application.py"
FLASK_DEBUG=1
```

- For Linux/macOS users, you should install [pyenv](https://github.com/pyenv/pyenv)
to manage your Python versions so you don't conflict with your System python, but
this is optional.

- Verify you have python **3.6** or later intalled and pipenv.
`pip install pipenv`

 - Install python dependencies
`pipenv install`

- Start python environment `pipenv shell`

- Create Database `python manage.py db init`

- Create Migration `python manage.py db migrate`

- Run Migration `python manage.py db upgrade`

- Start flask app `python -m flask run`

- Now proceed with starting node server for Vue.

# Instructions for Vue

Ensure vue-cli installed globally with either npm or yarn

- `npm install -g @vue/cli`
- `yarn global add @vue/cli`


Ensure vue-ui installed globally


```
yarn install
```

## Serving

### Use vue-ui ( recommended )

```
vue-ui
```

### Use yarn
```
yarn serve
```

## Build for production
```
yarn build
```

Builds will be made in the root of the repository in a folder called dist. This folder should not be commited to any repos.

# Python Unit Tests

```
pytest
```
