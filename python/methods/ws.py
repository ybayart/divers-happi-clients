from imports import *

def init():
	try:
		notify2.init('Happi client')
	except:
		pass

def send(title, content):
	try:
		n = notify2.Notification(title, content, "notification-message-im")
		n.set_urgency(notify2.URGENCY_CRITICAL)
		n.show()
	except:
		pass

def on_message(ws, message):
	try:
		data = json.loads(message)
		if data['type'] == 'message':
			send(data['title'], data['content'])
			ws.send(json.dumps({'type': 'confirm', 'id': data['id']}))
	except:
		pass

def on_open(ws):
	def run(*args):
		try:
			while 42:
				time.sleep(10)
				ws.send(json.dumps({'type': 'ping'}))
			time.sleep(1)
			ws.close()
		except:
			pass
	thread.start_new_thread(run, ())


def launch(g_data):
#	websocket.enableTrace(True)
	init()
	while 42:
		try:
			ws = websocket.WebSocketApp("wss://happi.hexanyn.fr/ws/",
									  on_message = on_message,
									  on_open = on_open,
									  header=["Authorization: Token {}".format(g_data['token'])])
#			thread.start_new_thread(ws.run_forever, ())
			ws.run_forever()
#			sys.exit()
		except:
			pass
		time.sleep(5)
	
#	running = True
#	try:
#		while running:
#			pass
#	except KeyboardInterrupt:
#		sys.exit()
