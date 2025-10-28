from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
from urllib.parse import parse_qs
import json

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
led_pins = [17, 27, 22]
pwms = []
for pin in led_pins:
	GPIO.setup(pin, GPIO.OUT)
	p = GPIO.PWM(pin, 1000)  # 1 kHz PWM
	p.start(0)
	pwms.append(p)

brightness = [0, 0, 0]  # store LED brightness %

# --- HTML + JavaScript ---
def make_page():
	return f"""<!DOCTYPE html>
<html>
<head>
	<title>LED Brightness Control</title>
	<style>
		body {{ font-family: Arial; margin: 40px; }}
		#interface {{
			border: 5pt solid black;
			padding: 25px;
			width: 400px;
			border-radius: 12px;
			box-shadow: 4px 4px 10px rgba(0,0,0,0.2);
		}}
		h2 {{ margin-bottom: 20px; }}
		.slider-container {{ margin-bottom: 25px; }}
		.slider-label {{ display: inline-block; width: 80px; }}
	</style>
</head>
<body>
	<h2>LED Brightness Control</h2>
	<div class="slider-container">
		<span class="slider-label">LED 1:</span>
		<input type="range" min="0" max="100" value="{brightness[0]}" id="led0" oninput="updateLED(0, this.value)">
		<span id="val0">{brightness[0]}</span>%
	</div>
	<div class="slider-container">
		<span class="slider-label">LED 2:</span>
		<input type="range" min="0" max="100" value="{brightness[1]}" id="led1" oninput="updateLED(1, this.value)">
		<span id="val1">{brightness[1]}</span>%
	</div>
	<div class="slider-container">
		<span class="slider-label">LED 3:</span>
		<input type="range" min="0" max="100" value="{brightness[2]}" id="led2" oninput="updateLED(2, this.value)">
		<span id="val2">{brightness[2]}</span>%
	</div>

	<script>
		function updateLED(led, val) {{
			document.getElementById("val" + led).innerText = val;
			fetch("/", {{
				method: "POST",
				headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
				body: "led=" + led + "&level=" + val
			}})
			.then(res => res.json())
			.then(data => {{
				for (let i = 0; i < 3; i++) {{
					document.getElementById("val" + i).innerText = data.brightness[i];
					document.getElementById("led" + i).value = data.brightness[i];
				}}
			}})
			.catch(err => console.error("Error:", err));
		}}
	</script>
</body>
</html>
"""

# --- Request Handler ---
class LEDHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(make_page().encode())

	def do_POST(self):
		length = int(self.headers['Content-Length'])
		body = self.rfile.read(length).decode()
		data = parse_qs(body)

		try:
			idx = int(data['led'][0])
			level = int(data['level'][0])
			brightness[idx] = level
			pwms[idx].ChangeDutyCycle(level)
		except:
			pass

		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write(json.dumps({"brightness": brightness}).encode())

# --- Server setup ---
if __name__ == "__main__":
	server = HTTPServer(("", 8080), LEDHandler)
	print("Server running on http://localhost:8080")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		for p in pwms:
			p.stop()
		GPIO.cleanup()
		server.server_close()
