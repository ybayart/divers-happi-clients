import websocket
try:
	import thread
except ImportError:
	import _thread as thread
import time, sys, os

def on_message(ws, message):
	if message != "pong":
		print(message)

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")

def on_open(ws):
	def run(*args):
		while 42:
			time.sleep(10)
			ws.send("ping")
		time.sleep(1)
		ws.close()
		print("thread terminating...")
	thread.start_new_thread(run, ())


if __name__ == "__main__":
#	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://happi.hexanyn.fr/ws/",
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close,
							  on_open = on_open,
							  header=["Authorization: Token {}".format(os.environ.get('HAPPI_TOKEN'))])
	thread.start_new_thread(ws.run_forever, ())
	
	print('tasoeur')
	running = True
	try:
		while running:
			pass
	except KeyboardInterrupt:
		sys.exit()
