from imports import *
from . import date
from . import invite

def choice_slot(g_data, create=True):
	slots = get_happi('users/{}/slots/'.format(g_data['user']['id']))
	if slots.status_code != 200:
		try:
			print(json_formatted(slots.json()))
		except:
			print(red("An error occured (status code: {})".format(slots.status_code)))
		return None
	slots = slots.json()
	slots_dict = dict()
	for slot in slots['results']: slots_dict[datetime.datetime.strptime(slot['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M | ') + slot['activity']] = slot
	try:
		choices = sorted(list(slots_dict), reverse=True)
		if create and g_data['me']['id'] == g_data['user']['id']:
			choices = ['Create one'] + choices
		if choices:
			slot = print_inquirer('Select a slot', choices)
		else:
			print(red('No slot to display\n'))
			return None
	except KeyboardInterrupt:
		return None
	return slot if slot == 'Create one' else slots_dict[slot]

def slots(g_data):
	slot = choice_slot(g_data)
	if slot != None:
		if slot == 'Create one':
			create_slot(g_data)
		else:
			display_slot(g_data, slot)

def display_slot(g_data, slot):
	print(json_formatted(slot))
	actions = {
		'See invitations': {'index': 1, 'func': invite.slot_invites},
		red('Delete'): {'index': 2, 'func': delete_slot},
	}
	try:
		action = print_inquirer("Select an action", get_ordered_keys(actions))
	except KeyboardInterrupt:
		return None
	try:
		if action in actions:
			command = actions[action]['func']
			command(g_data, slot)
		else:
			print(red('Select a valid action!'))
			menu()
	except:
		None

def create_slot(g_data):
	date_in = datetime.datetime.utcnow().replace(second=0, microsecond=0)
	to_ex = True
	date.date_disclaimer()
	while to_ex:
		ret, tmp = date.choice_date(date_in)
		if ret == True:
			date_in = tmp
			break
		elif ret == None:
			to_ex = False
			break
	while to_ex:
		ret, tmp = date.choice_time(date_in)
		if ret == True:
			date_in = tmp
			break
		elif ret == None:
			to_ex = False
			break
	if to_ex:
		try:
			activity = input('Activity> ')
		except:
			print('\n')
			to_ex = False
	if to_ex:
		print(yellow('-- Sum Up -- '))
		print(yellow('|   date:  '), blue(date_in.strftime('%H:%M %d/%m/%y')))
		print(yellow('| activity:'), blue(activity))
		try:
			resp = input('Informations are correct? [Y/n]: ')
			if resp.lower() in ['', 'y', 'yes']:
				print(green('Adding...'))
				req = post_happi('slots/', {'date': date_in.isoformat(), 'activity': activity})
				print('')
				if req.status_code == 201:
					display_slot(g_data, req.json())
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

def delete_slot(slot, g_data=None):
	req = delete_happi("slots/{}/".format(slot['id']))
	if req.status_code == 204:
		print(green('Deleted'))
	else:
		try:
			print(json_formatted(req.json()))
		except:
			print(red("An error occured (status code: {})".format(req.status_code)))
