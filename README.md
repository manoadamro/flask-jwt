# flask-jwt
[![CircleCI](https://circleci.com/gh/manoadamro/flask-jwt.svg?style=svg)](https://circleci.com/gh/manoadamro/flask-jwt)

## Supported Versions

- 3.6
- 3.7

## Usage

TO DO

## Installation

```
pip3 install --upgrape pip
pip3 install git+http://github.com/manoadamro/flask-jwt
```

## Contributing

Try to make pull requests that fulfill a single purpose (don't try to do loads of things at once)

clone the repo:
```
git clone http://github.com/manoadamro/flask-jwt
```

change to flask-jwt directory:
```
cd flask-jwt
```

install tox:
```
pip3 install tox
```

run the tests:
```
# for python 3.6
tox -e py36

# for python 3.7
tox -e py37

# for all of the above
tox
```

run black:
```
black ./tests/ ./flask_jwt
```

create a pull request!
