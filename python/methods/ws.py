from imports import *

def notification(title, content):
	n = notify2.Notification(title, content, "notification-message-im")
	n.show()

def on_message(ws, message):
	if message != "pong":
		notification("New message", message)

def on_error(ws, error):
	notification("Error", error)

def on_close(ws):
	nofitication("close", "### closed ###")

def on_open(ws):
	def run(*args):
		while 42:
			time.sleep(10)
			ws.send("ping")
		time.sleep(1)
		ws.close()
	thread.start_new_thread(run, ())


def launch(g_data):
#	websocket.enableTrace(True)
	notify2.init("Happi client")
	ws = websocket.WebSocketApp("wss://happi.hexanyn.fr/ws/",
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close,
							  on_open = on_open,
							  header=["Authorization: Token {}".format(g_data['token'])])
	thread.start_new_thread(ws.run_forever, ())
	
#	running = True
#	try:
#		while running:
#			pass
#	except KeyboardInterrupt:
#		sys.exit()
