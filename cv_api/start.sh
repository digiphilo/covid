curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv -o state.csv
curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv -o county.csv
export FLASK_RUN_PORT=$PORT && flask run --host=0.0.0.0
