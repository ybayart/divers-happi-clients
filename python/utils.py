from imports import *

# COLORS
def red(str): return "\033[91m{}\033[0m".format(str)
def green(str): return "\033[92m{}\033[0m".format(str)
def yellow(str): return "\033[93m{}\033[0m".format(str)
def blue(str): return "\033[94m{}\033[0m".format(str)
def pink(str): return "\033[95m{}\033[0m".format(str)

def json_formatted(value): return highlight(json.dumps(value, indent=4), JsonLexer(), TerminalFormatter())

def strbar(): return yellow("= - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - =")

def print_inquirer(message="Select a choice", choices=[]):
	print(strbar())
	questions = [
		inquirer.List('action',
			message=message,
			choices=choices,
		),
	]
	return inquirer.prompt(questions, raise_keyboard_interrupt=True)['action']

def get_ordered_keys(data):
	data_order = dict()
	for item in data:
		data_order[data[item]['index']] = item
	data_out = list()
	for item in sorted(data_order):
		data_out.append(data_order[item])
	return data_out

BASE_URL = 'https://happi.hexanyn.fr/'
API_URL = BASE_URL + 'api/'
LOGIN_URL = BASE_URL + 'api-token-auth/'

token = None

def auth_happi(g_data):
	USERNAME = input('Username: ')
	PASSWD = getpass.getpass()

	req = requests.post(LOGIN_URL, data = {'username': USERNAME, 'password': PASSWD})
	
	if req.status_code == 200:
		g_data['token'] = req.json()['token']

def get_happi(path, base_token=token):
	global token

	if base_token != None:
		token = base_token
	req = requests.get("{}{}".format(API_URL, path), headers={"Authorization": "Token {}".format(token)})
	return req

def post_happi(path, data={}, base_token=token):
	global token

	if base_token != None:
		token = base_token
	req = requests.post("{}{}".format(API_URL, path), headers={"Authorization": "Token {}".format(token)}, data = data)
	return req

def patch_happi(path, data={}, base_token=token):
	global token

	if base_token != None:
		token = base_token
	req = requests.patch("{}{}".format(API_URL, path), headers={"Authorization": "Token {}".format(token)}, data = data)
	return req

def delete_happi(path, base_token=token):
	global token

	if base_token != None:
		token = base_token
	req = requests.delete("{}{}".format(API_URL, path), headers={"Authorization": "Token {}".format(token)})
	return req

def check_auth(g_data):
	global token

	token = g_data['token']
	req = get_happi('me/')

	if req.status_code != 200:
		print(red('Unable to connect with your credentials, please check & try again'))
		return None

	print("You can use this script with '{} {}'".format(sys.argv[0], token))
	return req
