import csv

from flask import Flask, escape, request, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/api')
def index():
    return render_template('index.html')

@app.route('/api/timeline/counties')
def timeline_counties():
    return process_country_county(read_macro('county'), request.args.get('mode', None))

@app.route('/api/timeline/counties/<state>')
def timeline_counties_state(state):
    return process_state_county(read_macro('county'), state, None, request.args.get('mode', None))

@app.route('/api/timeline/counties/<state>/<county>')
def timeline_counties_state_county(state, county):
    return process_state_county(read_macro('county'), state, county, request.args.get('mode', None))

@app.route('/api/timeline/states')
def timeline_states():
    return country_view(read_macro('country'), request.args.get('mode', None))

@app.route('/api/timeline/states/<state>')
def timeline_state(state):
    return state_view(read_macro('country'), state, request.args.get('mode', None))

@app.route('/api/timeline/states/<state>/counties')
def timeline_state_counties(state):
    return process_state_county(read_macro('county'), state, None, request.args.get('mode', None))

@app.route('/api/timeline/states/<state>/counties/<county>')
def timeline_state_county(state, county):
    return process_state_county(read_macro('county'), state, county, request.args.get('mode', None))

def state_view(data, state_filter, mode_filter):
    dataset = {}
    data = filter_country_state(data, state_filter)
    for row in data:
            dataset[row[0]] = process_mode_state(row, mode_filter)
    return dataset

def country_view(data, mode_filter):
    dataset = {}
    for row in data:
        if row[1] not in dataset:
            dataset[row[1]] = {}
        dataset[row[1]][row[0]] = process_mode_state(row, mode_filter)
    return dataset

def filter_country_state(data, state_filter):
    result = []
    for row in data:
        if str_normalize(row[1]) == str_normalize(state_filter):
            result.append(row)
    return result

def process_state_county(data, state_filter, county_filter, mode_filter):
    data = filter_state(data, state_filter)
    if county_filter:
        return process_county_data(data, county_filter, mode_filter)
    else:
        return process_state_data(data, mode_filter)

def process_county_data(data, county_filter, mode_filter):
    dataset = {}
    for row in data:
        if row[1].replace(' ','').lower().capitalize() == county_filter.replace(' ','').lower().capitalize():
            dataset[row[0]] = process_mode_county(row, mode_filter)
            if mode_filter == 'cases':
                dataset[row[0]] = row[4]
            elif mode_filter == 'deaths':
                dataset[row[0]] = row[5]
            else:
                dataset[row[0]] = {'cases': row[4], 'deaths': row[5]}
    return dataset

def process_state_data(data, mode_filter):
    dataset = {}
    for row in data:
        if row[1] not in dataset:
            dataset[row[1]] = {}
        dataset[row[1]][row[0]] = process_mode_county(row, mode_filter)
    return dataset

def process_country_county(data, mode_filter):
    dataset = {}
    for row in data:
        if row[2] not in dataset:
            dataset[row[2]] = {}
        print(row)
        if row[1] not in dataset[row[2]]:
            dataset[row[2]][row[1]] = {}
        dataset[row[2]][row[1]][row[0]] = process_mode_county(row, mode_filter)
    return dataset

def process_mode_state(row, mode_filter):
    print(row)
    if mode_filter == 'cases':
        return int(row[3])
    elif mode_filter == 'deaths':
        return int(row[4])
    else:
        return {'cases': int(row[3]), 'deaths': int(row[4])}

def process_mode_county(row, mode_filter):
    if mode_filter == 'cases':
        return int(row[4])
    elif mode_filter == 'deaths':
        return int(row[5])
    else:
        return {'cases': int(row[4]), 'deaths': int(row[5])}

def filter_state(data, state_filter):
    result = []
    for row in data:
        print(state_filter.replace(' ','').lower().capitalize())
        print(row[2])
        if row[2].replace(' ','').lower().capitalize() == state_filter.replace(' ','').lower().capitalize():
            result.append(row)
    return result

def str_normalize(words):
    return words.replace(' ','').lower().capitalize()

def read_macro(macro):
    cv_data = []
    with open(get_macro_file(macro), newline='') as data_file:
        data_reader = csv.reader(data_file)
        for row in data_reader:
            cv_data.append(row)
    cv_data.pop(0)
    return cv_data

def get_macro_file(macro):
    if macro == 'county':
        file = 'county.csv'
    if macro == 'state':
        file = 'county.csv'
    elif macro == 'country':
        file = 'state.csv'
    if file:
        return file
    else:
        abort(500)