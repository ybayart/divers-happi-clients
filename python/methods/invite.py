from imports import *
from . import slot
from . import user

def choice_invite(g_data, create=True, invites=None, receiver=True):
	color = [red, green]
	if invites == None:
		invites = get_happi('users/{}/invites/'.format(g_data['user']['id']))
		if invites.status_code != 200:
			try:
				print(json_formatted(invites.json()))
			except:
				print(red("An error occured (status code: {})".format(invites.status_code)))
			return None
		invites = invites.json()
	invites_dict = dict()
	for invite in invites['results']:
		index = [datetime.datetime.strptime(invite['slot']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M'), invite['slot']['user']['username'], color[invite['accepted']](invite['slot']['activity']), color[invite['accepted']](invite['user']['username'])]
		if receiver:
			index = "{0} | {1}: {2}".format(*index)
		else:
			index = "{3}".format(*index)
		invites_dict[index] = invite
	try:
		choices = sorted(list(invites_dict), reverse=True)
#		if create and g_data['me']['id'] == g_data['user']['id']:
		choices = ['Create one'] + choices
		if choices:
			invite = print_inquirer('Select an invite', choices)
		else:
			print(red('No invite to display\n'))
			return None
	except KeyboardInterrupt:
		return None
	return invite if invite == 'Create one' else invites_dict[invite]
	
def invites(g_data):
	invite = choice_invite(g_data)
	if invite != None:
		if invite == 'Create one':
			create_invite(g_data)
		else:
			display_invite(g_data, invite)

def display_invite(g_data, invite):
	print(json_formatted(invite))
	actions = {
		red('Delete'): {'index': 2, 'func': delete_invite},
	}
	if invite['user']['id'] == g_data['user']['id']:
		if invite['accepted']:
			actions['Decline'] = {'index': 1, 'func': decline_invite}
		else:
			actions['Accept'] = {'index': 1, 'func': accept_invite}
	try:
		action = print_inquirer("Select an action", get_ordered_keys(actions))
	except KeyboardInterrupt:
		return None
	try:
		if action in actions:
			command = actions[action]['func']
			command(invite['id'])
		else:
			print(red('Select a valid action!'))
			menu()
	except:
		None

def create_invite(g_data, slot_in=None):
	to_ex = True
	if to_ex and slot_in == None:
		slot_in = slot.choice_slot(g_data, create=False)
		if slot_in == None:
			to_ex = False
	if to_ex:
		user_in = user.choice_user()
		if user_in == None:
			to_ex = False
	if to_ex:
		try:
			date_slot = datetime.datetime.strptime(slot_in['date'], '%Y-%m-%dT%H:%M:%SZ')
		except:
			try:
				date_slot = datetime.datetime.strptime(slot_in['date'], '%Y-%m-%dT%H:%M:%S')
			except:
				date_slot = slot_in['date']
				to_ex = False
		if to_ex: date_slot = date_slot.strftime('%Y-%m-%d %H:%M')
		print(yellow('-- Sum Up -- '))
		print(yellow('| slot:'), blue("{} | {}".format(date_slot, slot_in['activity'])))
		print(yellow('| user:'), blue(user_in['username']))
		try:
			resp = input('Informations are correct? [Y/n]: ')
			if resp.lower() in ['', 'y', 'yes']:
				req = post_happi('invites/', {'slot': slot_in['id'], 'user': user_in['id']})
				print('')
				if req.status_code == 201:
					print(green('Added'))
				else:
					try:
						print(json_formatted(req.json()))
					except:
						print(red("An error occured (status code: {})".format(req.status_code)))
				print('\n')
			else:
				raise
		except:
			print(red('\nOperation cancelled\n'))

def accept_invite(invite_id):
	req = patch_happi("invites/{}/".format(invite_id), data={'accepted': True})
	if req.status_code == 200:
		print(green('Accepted!'))
	else:
		try:
			print(json_formatted(req.json()))
		except:
			print(red("An error occured (status code: {})".format(req.status_code)))

def decline_invite(invite_id):
	req = patch_happi("invites/{}/".format(invite_id), data={'accepted': False})
	if req.status_code == 200:
		print(green('Declined!'))
	else:
		try:
			print(json_formatted(req.json()))
		except:
			print(red("An error occured (status code: {})".format(req.status_code)))

def delete_invite(invite_id):
	req = delete_happi("invites/{}/".format(invite_id))
	if req.status_code == 204:
		print(green('Deleted'))
	else:
		try:
			print(json_formatted(req.json()))
		except:
			print(red("An error occured (status code: {})".format(req.status_code)))

def slot_invites(g_data, slot):
	invites = get_happi("slots/{}/invites/".format(slot['id'])).json()
	invite = choice_invite(g_data, invites=invites, receiver=False)
	if invite == "Create one":
		create_invite(g_data, slot_in=slot)
	else:
		display_invite(g_data, invite)
