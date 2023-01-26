"""
    @author Deep
    @contributor  
"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# * Trigger and Echo Pin on the RPi in BCM mode
trigPin = 23
echoPin = 24

GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

try:
    while True:
        # * Start the pulse to get the sensor to send the ping
        GPIO.output(trigPin, 0)     # Cutting out power from the trigger pin
        time.sleep(2E-6)            # Sleep for 2 micro second i.e. 2 X 10^-6
        GPIO.output(trigPin, 1)     # Passing power to the trigger pin

        time.sleep(10E-6)           # Sleep for 10 micro second i.e. 10 X 10^-6
        
        # * Communication complete to send ping
        GPIO.output(trigPin, 0)     # Cutting out power from the trigger pin

        # * Now wait till echo pin goes high to start the timer, meaning that the ping has been sent
        while GPIO.input(echoPin) == 0:
            pass
        
        echoStartTime = time.time()

        # * Now wait till echo pin to go down to zero 
        while GPIO.input(echoPin) == 1:
            pass

        echoStopTime = time.time()

        # * Travel time taken by ping to go to the obstacle and back to the sensor
        pingTravelTime = echoStopTime - echoStartTime

        # * Use time to calculate the distance to the target
        # * Speed of sound at 28℃ is 347.8 m/s
        # * Source: https://www.omnicalculator.com/physics/speed-of-sound
        totalDistance = 34780 * pingTravelTime

        # * Divide in half since the time of travel is out and back
        targetDistance = totalDistance / 2  # Distance in cm

        print(f"{round(targetDistance, 1)} cm")

        time.sleep(0.2)

except:
    GPIO.cleanup()
    print('GPIO Cleaned!')