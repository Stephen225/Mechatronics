import socket
import RPi.GPIO as GPIO
import threading
from time import sleep

GPIO.setmode(GPIO.BCM)

#pins or something
pins = (16,20,21)
for p in pins: GPIO.setup(p,GPIO.OUT)
pwms = [GPIO.PWM(pin, 500) for pin in pins]
for thing in pwms:
	thing.start(0)
led1, led2, led3 = 0, 2, 100

def web_page():
	html = """
		<html>
        <head> <title>leds and stuff</title>
        <style> body{
        	border: 2px solid black;
			width: fit_content;
        	}</style>
		</head>
		<body>
		<form action="/" method="POST">
		Brightness Level: <br>
		<input type="range" id="slider" name="slider" min="0" max="100" value="50">
        <br><br>
        Select LED: <br>
        <input type="radio" id="button1" name="button" value="led1">
        <label for="led1">LED 1 (
        """ + str(led1) + """%)</label><br>
        <input type="radio" id="button2" name="button" value="led2">
        <label for="led2">LED 2 (
        """ + str(led2) + """%)</label><br>
        <input type="radio" id="button3" name="button" value="led3">
        <label for="led3">LED 3 (
        """ + str(led3) + """%)</label><br>
        <br>
        <input type="submit" id="submit" name="submit" value="Change Brightness">
        </form>
        </body>
		</html>
		"""
	return (bytes(html, 'utf-8'))

def parsePOSTdata(data):
	data_dict = {}
	idx = data.find('\r\n\r\n')+4
	data = data[idx:]
	data_pairs = data.split('&')
	for pair in data_pairs:
		key_val = pair.split('=')
		if len(key_val) == 2:
			data_dict[key_val[0]] = key_val[1]
	return data_dict

def serve_web_page():
	global led1, led2, led3
	while True:
		print('Waiting for connection...')
		conn, (client_ip, client_port) = s.accept()     # blocking call
		client_message = conn.recv(1024).decode('utf-8')               # read request (required even if none)
		print(f'Connection from {client_ip}')
		data_dict = parsePOSTdata(client_message)
		print(data_dict)
		if 'button' in data_dict.keys():
			if data_dict["button"] == 'led1':
				led1 = int(data_dict["slider"])
			elif data_dict["button"] == 'led2':
				led2 = int(data_dict["slider"])
			elif data_dict["button"] == 'led3':
				led3 = int(data_dict["slider"])
		'''
		if 'led1' in data_dict.keys():   # make sure data was posted
			led1 = data_dict["slider"]
			print(led1)
		else:   # web page loading for 1st time so start with 0 for the LED byte
			led1 = '0'
		if 'led2' in data_dict.keys():   # make sure data was posted
			led2 = data_dict["slider"]
			print(led2)
		else:   # web page loading for 1st time so start with 0 for the LED byte
			led2 = '0'
		if 'led3' in data_dict.keys():   # make sure data was posted
			led3 = data_dict["slider"]
			print(led3)
		else:   # web page loading for 1st time so start with 0 for the LED byte
			led3 = '0'
		'''
		conn.send(b'HTTP/1.1 200 OK\n')         # status line
		conn.send(b'Content-type: text/html\n') # header (content type)
		conn.send(b'Connection: close\r\n\r\n') # header (tell client to close at end)
        # send body in try block in case connection is interrupted:
		try:
			conn.sendall(web_page())                  # body
		finally:
			conn.close()

		#set led pins to correct value
		pwms[0].ChangeDutyCycle(led1)
		pwms[1].ChangeDutyCycle(led2)
		pwms[2].ChangeDutyCycle(led3)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP-IP socket
s.bind(('', 8080))
s.listen(3)  # up to 3 queued connections

webpageThread = threading.Thread(target=serve_web_page)
webpageThread.daemon = True
webpageThread.start()

try:
	while True:
		pass
except:
	print('Joining webpageThread')
	webpageThread.join()
	print('Closing socket')
	s.close()