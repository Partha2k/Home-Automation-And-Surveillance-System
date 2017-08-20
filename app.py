import RPi.GPIO as GPIO
from flask import Flask, render_template, request, Response
from webcamvideostream import WebcamVideoStream
import cv2
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   18 : {'name' : 'FAN', 'state' : GPIO.LOW},
   17 : {'name' : 'LIGHT', 'state' : GPIO.LOW},
   22 : {'name' : 'TV', 'state' : GPIO.LOW},
   23 : {'name' : 'MUSIC', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
      GPIO.setwarnings(False)
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, GPIO.LOW)

@app.route("/", methods=['POST','GET'])
def main():
   if request.method == 'POST':
      """Video streaming home page."""
      return render_template('index1.html')
   else:
   # For each pin, read the pin state and store it in the pins dictionary:
       for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
       templateData = {
          'pins' : pins
          }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>", methods=['POST','GET'])
def action(changePin, action):
    if request.method == 'POST':
       """Video streaming home page."""
       return render_template('index1.html')
    else:
       # Convert the pin from the URL into an integer:
       changePin = int(changePin)
       # Get the device name for the pin being changed:
       deviceName = pins[changePin]['name']
       # If the action part of the URL is "on," execute the code indented below:
       if action == "on":
          # Set the pin high:
          GPIO.output(changePin, GPIO.HIGH)
          # Save the status message to be passed into the template:
          message = "Turned " + deviceName + " on."
       if action == "off":
          GPIO.output(changePin, GPIO.LOW)
          message = "Turned " + deviceName + " off."

       # For each pin, read the pin state and store it in the pins dictionary:
       for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)

       # Along with the pin dictionary, put the message into the template data dictionary:
       templateData = {
          'pins' : pins
       }

    return render_template('main.html', **templateData)

#@app.route("/")
#def index():
#    """Video streaming home page."""
#    return render_template('index1.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame)

        # print("after get_frame")
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tostring() + b'\r\n')
        else:
            print("frame is none")



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(WebcamVideoStream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
