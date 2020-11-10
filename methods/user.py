from imports import *

def choice_user():
	users = req_happi('users/').json()
	users_dict = dict()
	for user in users['results']: users_dict[user['username']] = user['id']
	try:
		user = print_inquirer('Select an user', sorted(users_dict.keys()))
	except KeyboardInterrupt:
		return None
	return {'id': users_dict[user], 'username': user}

def users(g_data):
	user = req_happi("users/{}".format(g_data['user']['id'])).json()
	print(json_formatted(user))

def friends(g_data):
	friends = req_happi("users/{}/friends/".format(g_data['user']['id'])).json()
	try:
		friends = friends['results'][0]['friends']
		print(yellow("{} friends:\n|".format(g_data['user']['username'])), yellow("\n| ").join(sorted(blue(user['username']) for user in friends)), "\n")
	except:
		print(json_formatted(friends))
	
def slots(g_data):
	slots = req_happi("users/{}/slots/".format(g_data['user']['id'])).json()
	try:
		slots = slots['results']
	except:
		None
#	print(yellow("Slots:\n|"), yellow("\n| ").join(sorted(blue(user) for slot in slots)), "\n")
	print(json_formatted(slots))
	
def invites(g_data):
	invites = req_happi("users/{}/invites/".format(g_data['user']['id'])).json()
	try:
		invites = invites['results']
	except:
		None
#	print(yellow("Slots:\n|"), yellow("\n| ").join(sorted(blue(user) for slot in slots)), "\n")
	print(json_formatted(invites))

def switch_me(g_data):
	g_data['user'] = g_data['me']

def switch_user(g_data):
	ret_user = choice_user()
	if ret_user != None:
		g_data['user'] = ret_user
