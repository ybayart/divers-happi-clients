#! /usr/bin/python3

from imports import *

g_data = {
	'token': None,
	'f': Figlet(font="slant"),
	'me': None,
	'user': None,
}

def get_credential():
	global g_data
	if len(sys.argv) == 2:
		g_data['token'] = sys.argv[1]
	else:
		auth_happi(g_data)
	me = check_auth(g_data)
	if me == None:
		exit(1)
	g_data['me'] = me.json()['results'][0]
	g_data['user'] = {'id': g_data['me']['id'], 'username': g_data['me']['username']}
	print(strbar())
	print(yellow(g_data['f'].renderText("Hello {}".format(g_data['me']['username']))))

actions = {
	'User informations': {'index': 1, 'func': user.users},
	'User friends': {'index': 2, 'func': friend.friends},
	'User slots': {'index': 3, 'func': slot.slots},
	'User invitations': {'index': 4, 'func': invite.invites},
	'Select me': {'index': 5, 'func': user.switch_me},
	'Select other user': {'index': 6, 'func': user.switch_user},
}

def menu():
	global g_data
	print(yellow('Token user:'), blue(g_data['me']['username']))
	print(yellow('Current selected user:'), blue(g_data['user']['username']))
	try:
		action = print_inquirer("Select a category", get_ordered_keys(actions))
	except TypeError:
		exit(0)
	except KeyboardInterrupt:
		exit(0)
	try:
		if action in actions:
			command = actions[action]['func']
			command(g_data)
		else:
			print(red('Select a valid action!'))
			menu()
	except KeyboardInterrupt:
#		print(chr(27) + "[2J")
		menu()

if __name__ == "__main__":
	get_credential()
	while 42:
		menu()
