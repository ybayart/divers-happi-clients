from imports import *

def choice_user():
	users = get_happi('users/').json()
	users_dict = dict()
	for user in users['results']: users_dict[user['username']] = user['id']
	try:
		user = print_inquirer('Select an user', sorted(users_dict.keys()))
	except KeyboardInterrupt:
		return None
	return {'id': users_dict[user], 'username': user}

def users(g_data):
	user = get_happi("users/{}".format(g_data['user']['id'])).json()
	print(json_formatted(user))

def switch_me(g_data):
	g_data['user'] = g_data['me']

def switch_user(g_data):
	ret_user = choice_user()
	if ret_user != None:
		g_data['user'] = ret_user
