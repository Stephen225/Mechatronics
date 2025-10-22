import socket
import RPi.GPIO as GPIO
import threading
from time import sleep

GPIO.setmode(GPIO.BCM)

#pins or something
pins = (19,21,22)
for p in pins: GPIO.setup(p,GPIO.OUT)

led1, led2, led3 = 0, 2, 100

def web_page():
	html = """
		<html>
        <head> <title>leds and stuff</title>
        <style> body{ border: 1px solid black;}</style>
        </head>
        <body> Brightness Level: <br>
		<input type="range" id="slider" name="slider" min="0" max="100" value="50">
        <br><br>
        Select LED: <br>
        <input type="radio" id="button1" name="button" value="HIGH">
        <label for="led1">LED 1 (
        """ + led1 + """%)</label><br>
        <input type="radio" id="button2" name="button" value="HIGH">
        <label for="led2">LED 2 (
        """ + led2 + """%)</label><br>
        <input type="radio" id="button3" name="button" value="HIGH">
        <label for="led3">LED 3 (
        """ + led3 + """%)</label><br>
        <br>
        <input type="button" id="submit" name="submit" value="Change Brightness">
        </body>
		</html>
		"""
	return (bytes(html, 'utf-8'))

def serve_web_page():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP-IP socket
    s.bind(('', 80))
    s.listen(3)  # up to 3 queued connections
    try:
        while True:
            print('Waiting for connection...')
            conn, (client_ip, client_port) = s.accept()     # blocking call
            request = conn.recv(1024)               # read request (required even if none)
            print(f'Connection from {client_ip}')
            conn.send(b'HTTP/1.1 200 OK\n')         # status line
            conn.send(b'Content-type: text/html\n') # header (content type)
            conn.send(b'Connection: close\r\n\r\n') # header (tell client to close at end)
            # send body in try block in case connection is interrupted:
            try:
                conn.sendall(web_page())                  # body
            finally:
                conn.close()
    except:
        print('Closing socket')
        s.close()

webpageThread = threading.Thread(target=serve_web_page)
webpageThread.daemon = True
webpageThread.start()

while True:
    sleep(1)
    print('.')