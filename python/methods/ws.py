from imports import *

# Thread don't display anything
# it's running ?
class ws_receive(Thread):
	def __init__(self, ws):
		Thread.__init__(self)
		self.ws = ws

	async def run(self):
		while 42:
			resp = await self.ws.recv()
#			if resp != "pong":
			print(resp, file=sys.stderr)


async def hello():
	uri = "wss://happi.hexanyn.fr/ws/"
	header = {"Authorization": "Token {}".format(os.environ.get('HAPPI_TOKEN'))}
	async with websockets.client.connect(uri, extra_headers=header) as ws:
		announce = await ws.recv()
		print("< {}".format(announce))

#		receiver = ws_receive(ws)
#		receiver.start()

		while 42:
#			await ws.send("ping")
#			print('test')
			time.sleep(10)

try:
	asyncio.get_event_loop().run_until_complete(hello())
except:
	exit(0)
