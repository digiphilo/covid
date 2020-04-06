# covid
pandemic utilities


## Setup

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running It

```sh
cd covid
export FLASK_APP=app.py
flask run
```

Open http://localhost:5000/

## Development

```sh
cd covid
source venv/bin/activate
pylint --rcfile pylintrc cv_api/app.py
```
