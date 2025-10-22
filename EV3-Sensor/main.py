#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait
import socket

# Configuration constants
SERVER_PORT = 12345
MOTOR_SPEED = 200
READ_INTERVAL = 1000  # milliseconds

# Color mapping for easy conversion
COLOR_MAP = {
    Color.RED: 'RED',
    Color.GREEN: 'GREEN',
    Color.BLUE: 'BLUE',
    Color.YELLOW: 'YELLOW',
    Color.BLACK: 'BLACK',
    Color.WHITE: 'WHITE'
}

def initialize_devices():
    motor = Motor(Port.D)
    sensor = ColorSensor(Port.S1)
    motor.stop()  # Ensure motor is stopped at startup
    return motor, sensor

def setup_server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', SERVER_PORT))
    server.listen(1)
    
    brick.display.text("Waiting for client...")
    client, _ = server.accept()
    brick.display.text("Connected!")
    
    return server, client

def handle_color(sensor, client):
    color = sensor.color()
    color_str = COLOR_MAP.get(color)
    
    if color_str:
        try:
            client.send(color_str.encode())
            brick.display.text(color_str)
            return True
        except Exception as e:
            print(f"Color send error: {str(e)}")
            return False
    return True

def handle_motor_command(command, motor):
    if command == "START_MOTOR":
        motor.run(MOTOR_SPEED)
        brick.display.text("Motors Started")
    elif command == "STOP_MOTOR":
        motor.stop()
        brick.display.text("Motors Stopped")

def main():
    # Display initialization
    brick.display.clear()
    brick.display.text("Starting...")
    
    try:
        # Initial setup
        motor, sensor = initialize_devices()
        server, client = setup_server()
        
        # Main loop
        while True:
            # Color handling
            if not handle_color(sensor, client):
                break
                
            # Command handling
            try:
                data = client.recv(1024).decode('utf-8')
                handle_motor_command(data, motor)
            except Exception as e:
                print(f"Command reception error: {str(e)}")
                break
                
            wait(READ_INTERVAL)
            
    except Exception as e:
        brick.display.text(f"Error: {str(e)}")
        
    finally:
        # Cleanup and close
        motor.stop()
        client.close()
        server.close()

if __name__ == "__main__":
    main()
