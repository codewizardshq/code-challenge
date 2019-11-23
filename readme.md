# Instructions for Flask

- Before begining please create a .flaskenv file with the following contents

```
FLASK_ENV = "development"
FLASK_APP = "app"
# Uncomment this to debug:
FLASK_DEBUG=1
```

- Verify you have python 3.7 intalled and pipenv.
`pip install pipenv`

 - Install python dependencies
`pipenv install --dev`

- Start python environment `pipenv shell`

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
