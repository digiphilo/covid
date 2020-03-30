import csv
import us

from flask import Flask, escape, request, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/api')
def index():
    return render_template('index.html')

@app.route('/api/total/counties')
def total_counties():
    return process_counties_total(read_macro('county'), get_args(request))

@app.route('/api/total/counties/<state>')
def total_counties_state(state):
    return process_state_counties_total(read_macro('county'), state, None, get_args(request))

@app.route('/api/total/counties/<state>/<county>')
def  total_counties_state_county(state, county):
    return process_state_counties_total(read_macro('county'), state, county, get_args(request))

@app.route('/api/total/states')
def total_states():
    return country_view_total(read_macro('country'), get_args(request))

@app.route('/api/total/states/<state>')
def total_states_state(state):
    return state_view_total(read_macro('country'), state, get_args(request))

@app.route('/api/total/states/<state>/counties')
def total_states_state_counties(state):
    return process_state_counties_total(read_macro('county'), state, None, get_args(request))

@app.route('/api/total/states/<state>/counties/<county>')
def total_states_state_counties_county(state, county):
    return process_state_counties_total(read_macro('county'), state, county, get_args(request))

@app.route('/api/timeline/counties')
def timeline_counties():
    return process_country_county(read_macro('county'), get_args(request))

@app.route('/api/timeline/counties/<state>')
def timeline_counties_state(state):
    return process_state_county(read_macro('county'), state, None, get_args(request))

@app.route('/api/timeline/counties/<state>/<county>')
def timeline_counties_state_county(state, county):
    return process_state_county(read_macro('county'), state, county, get_args(request))

@app.route('/api/timeline/states')
def timeline_states():
    return country_view(read_macro('country'), get_args(request))

@app.route('/api/timeline/states/<state>')
def timeline_state(state):
    return state_view(read_macro('country'), state, get_args(request))

@app.route('/api/timeline/states/<state>/counties')
def timeline_state_counties(state):
    return process_state_county(read_macro('county'), state, None, get_args(request))

@app.route('/api/timeline/states/<state>/counties/<county>')
def timeline_state_county(state, county):
    return process_state_county(read_macro('county'), state, county, get_args(request))

def state_view_total(data, state_filter, args):
    data = filter_country_state(data, state_filter)
    result = process_mode(args, data[-1][3], data[-1][4])
    result = str(result) if isinstance(result, int) else result
    return result

def state_view(data, state_filter, args):
    result = {}
    key_row = get_key_row(args, 'country')
    data = filter_country_state(data, state_filter)
    for row in data: result[row[key_row]] = process_mode(args, row[3], row[4])
    return result

def country_view_total(data, args):
    dataset = {}
    key_row = get_key_row(args, 'country')
    for row in reversed(data):
        if row[key_row] not in dataset:
            dataset[row[key_row]] = process_mode(args, row[3], row[4])
    return dataset

def country_view(data, args):
    dataset = {}
    key_row = get_key_row(args, 'country')
    for row in data:
        if row[key_row] not in dataset: dataset[row[key_row]] = {}
        dataset[row[key_row]][row[0]] = process_mode(args, row[3], row[4])
    return dataset

def process_state_counties_total(data, state_filter, county_filter, args):
    data = filter_state(data, state_filter)
    if county_filter:
        result = process_county_data_total(data, county_filter, args)
        if isinstance(result, int): result = str(result)
        return result
    else:
        return process_state_data_total(data, args)

def process_state_data_total(data, args):
    dataset = {}
    for row in reversed(data):
        key_row = get_key_row(args, 'state')
        if row[key_row] and row[key_row] not in dataset:
            dataset[row[key_row]] = process_mode(args, row[4], row[5])
    return dataset

def process_state_county(data, state_filter, county_filter, args):
    data = filter_state(data, state_filter)
    if county_filter:
        return process_county_data(data, county_filter, args)
    else:
        return process_state_data(data, args)

def process_county_data_total(data, county_filter, args):
    for row in reversed(data):
        if compare_county(county_filter, row[1], row[3]):
            return process_mode(args, row[4], row[5])

def process_county_data(data, county_filter, args):
    dataset = {}
    for row in data:
        if compare_county(county_filter, row[1], row[3]):
            dataset[row[0]] = process_mode(args, row[4], row[5])
    return dataset

def process_state_data(data, args):
    dataset = {}
    key_row = get_key_row(args, 'state')
    for row in data:
        if row[key_row]:
            if row[key_row] not in dataset: dataset[row[key_row]] = {}
            dataset[row[key_row]][row[0]] = process_mode(args, row[4], row[5])
    return dataset

def process_counties_total(data, args):
    dataset = {}
    key_row = get_key_row(args, 'state')
    for row in reversed(data):
        state_key = get_state_key(args, row[2])
        if state_key not in dataset: dataset[state_key] = {}
        if row[key_row] not in dataset[state_key]:
            dataset[state_key][row[key_row]] = process_mode(args, row[4], row[5])
    return dataset

def process_country_county(data, args):
    dataset = {}
    key_row = get_key_row(args, 'state')
    for row in data:
        state_key = get_state_key(args, row[2])
        if state_key not in dataset:
            dataset[state_key] = {}
        if row[key_row] not in dataset[state_key]:
            dataset[state_key][row[key_row]] = {}
        dataset[state_key][row[key_row]][row[0]] = process_mode(args, row[4], row[5])
    return dataset

def process_mode(args, cases, deaths):
    if args['mode'] == 'cases': return int(cases)
    elif args['mode'] == 'deaths': return int(deaths)
    else: return {'cases': cases, 'deaths': deaths}

def filter_state(data, state_filter):
    result = []
    for row in data:
        if compare_state(state_filter, row[2]):
            result.append(row)
    return result

def filter_country_state(data, state_filter):
    result = []
    for row in data:
        if compare_state(state_filter, row[1]):
            result.append(row)
    return result

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

def get_args(request):
    return {'mode': request.args.get('mode', None),
            'fips': request.args.get('fipsKey', False)}

def compare_state(state_filter, entry):
    if str_normalize(entry) == str_normalize(state_filter):
        return True
    if us.states.lookup(state_filter) and us.states.lookup(state_filter).name == entry:
        return True
    return False

def compare_county(county_filter, entry, fips_entry):
    if str_normalize(entry) == str_normalize(county_filter):
        return True
    if county_filter == fips_entry:
        return True
    return False

def str_normalize(words):
    return words.replace(' ','').lower().capitalize()

def get_key_row(args, locale):
    if locale == 'state': key_row = 3 if args['fips'] else 1
    else: key_row = 2 if args['fips'] else 1
    return key_row

def get_state_key(args, state):
    if args['fips']: return us.states.lookup(state).fips
    else: return state
