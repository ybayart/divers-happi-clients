from imports import *

def date_disclaimer():
	print(yellow("Date selection, leave blank to validate displayed/actual time"))
	print(red("WARNING: Time here is in UTC format"))

def choice_date(date):
	try:
		date_in = input("Date ({})> ".format(date.strftime("%d/%m/%Y")))
		if date_in:
			date_in = date_in.split('/')
			date = date.replace(day=int(date_in[0]), month=int(date_in[1]), year=int(date_in[2]))
		return True, date
	except KeyboardInterrupt:
		print('\n')
		return None, date
	except:
		print(red("Unable to parse date"))
		return False, date

def choice_time(time):
	try:
		time_in = input("Time ({})> ".format(time.strftime("%H:%M")))
		if time_in:
			time_in = time_in.split(':')
			time = time.replace(hour=int(time_in[0]), minute=int(time_in[1]))
		return True, time
	except KeyboardInterrupt:
		print('\n')
		return None, time
	except:
		print(red("Unable to parse time"))
		return False, time
