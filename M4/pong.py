'''
What: Pong game using Turtle
Where: https://www.geeksforgeeks.org/create-pong-game-using-python-turtle/
Why: There are many versions of the Pong game and the main focus for this mini
project is to control one of the paddles using the Arduino IMU. Reusing already
existing code for the Pong game allows me to merge BLE connectivity code with
an already working solution to a Pong game. 
'''

# Import required library
import turtle
import asyncio
import struct
import time
import multiprocessing as mp
from bleak import BleakClient
from bleak import BleakScanner

uuid_value = '00002101-0000-1000-8000-00805f9b34fb'

class Pong:
    def __init__(self, ax):
        # Create screen
        self.sc = turtle.Screen()
        self.sc.title("Pong game")
        self.sc.bgcolor("white")
        self.sc.setup(width=1000, height=600)

        # Left paddle
        self.left_pad = turtle.Turtle()
        self.left_pad.speed(0)
        self.left_pad.shape("square")
        self.left_pad.color("black")
        self.left_pad.shapesize(stretch_wid=6, stretch_len=2)
        self.left_pad.penup()
        self.left_pad.goto(-400, 0)

        # Right paddle
        self.right_pad = turtle.Turtle()
        self.right_pad.speed(0)
        self.right_pad.shape("square")
        self.right_pad.color("black")
        self.right_pad.shapesize(stretch_wid=30, stretch_len=2)
        self.right_pad.penup()
        self.right_pad.goto(400, 0)

        # Ball of circle shape
        self.hit_ball = turtle.Turtle()
        self.hit_ball.speed(40)
        self.hit_ball.shape("circle")
        self.hit_ball.color("blue")
        self.hit_ball.penup()
        self.hit_ball.goto(0, 0)
        self.hit_ball.dx = 6
        self.hit_ball.dy = -6

        # Initialize the score
        self.left_player = 10
        # right_player = 0

        # Displays the score
        self.sketch = turtle.Turtle()
        self.sketch.speed(0)
        self.sketch.color("blue")
        self.sketch.penup()
        self.sketch.hideturtle()
        self.sketch.goto(0, 260)
        self.sketch.write("Left_player : {}".format(self.left_player), align="center", font=("Courier", 24, "normal"))

        self.update_screen(ax)

    # Functions to move paddle vertically
    def mainPaddleMovement(self, ax):
        print(ax.value)
        if ax.value < -0.3:
            self.paddleaup()
        if ax.value > 0.3:
            self.paddleadown()

    def paddleaup(self):
        y = self.left_pad.ycor()
        y += 10
        self.left_pad.sety(y)

    def paddleadown(self):
        y = self.left_pad.ycor()
        y -= 10
        self.left_pad.sety(y)
    
    def update_screen(self, ax):
        while True:
            self.sc.update()
            self.mainPaddleMovement(ax)

            self.hit_ball.setx(self.hit_ball.xcor()+self.hit_ball.dx)
            self.hit_ball.sety(self.hit_ball.ycor()+self.hit_ball.dy)

            # Checking borders
            if self.hit_ball.ycor() > 280:
                self.hit_ball.sety(280)
                self.hit_ball.dy *= -1

            if self.hit_ball.ycor() < -280:
                self.hit_ball.sety(-280)
                self.hit_ball.dy *= -1

            # if hit_ball.xcor() > 500:
            # 	hit_ball.goto(0, 0)
            # 	hit_ball.dy *= -1
            # 	left_player += 1
            # 	sketch.clear()
            # 	sketch.write("Left_player : {} Right_player: {}".format(left_player, right_player), align="center", font=("Courier", 24, "normal"))

            if self.hit_ball.xcor() < -500:
                self.hit_ball.goto(0, 0)
                self.hit_ball.dy *= -1
                self.left_player -= 1
                self.sketch.clear()
                self.sketch.write("Left_player : {}".format(self.left_player), align="center", font=("Courier", 24, "normal"))

            # Paddle ball collision
            if (self.hit_ball.xcor() > 360 and self.hit_ball.xcor() < 370) and (self.hit_ball.ycor() < self.right_pad.ycor() + 300 and self.hit_ball.ycor() > self.right_pad.ycor() - 300):
                self.hit_ball.setx(360)
                self.hit_ball.dx *= -1
                
            if (self.hit_ball.xcor() < -360 and self.hit_ball.xcor() > -370) and (self.hit_ball.ycor() < self.left_pad.ycor() + 60 and self.hit_ball.ycor() > self.left_pad.ycor() - 60):
                self.hit_ball.setx(-360)
                self.hit_ball.dx *= -1


async def connect_BLE():
    print('Looking for Rod Nano 33 IoT Peripheral Device...')

    found = False
    while True:
        devices = await BleakScanner.discover()
        for d in devices:     
            if d.name and 'Rod Nano 33 IoT' in d.name:
                print('Found Rod Nano 33 IoT Peripheral')
                found = True
                async with BleakClient(d.address) as client:
                    print(f'Connected to {d.address}')

                    manager = mp.Manager()
                    ax = manager.Value('d', 0.0)
                    pong_proc = mp.Process(target=Pong, args=(ax,))
                    pong_proc.start()

                    while True:
                        sensorByteVal = await client.read_gatt_char(uuid_value)
                        ax.value = struct.unpack('<f', sensorByteVal)[0]
                        
                        time.sleep(0.02)

                pong_proc.join()

        if found:
            break
 

if __name__ == "__main__":
    try:
        asyncio.run(connect_BLE())
    except KeyboardInterrupt:
        print('\nReceived Keyboard Interrupt')
    finally:
        print('Program finished')



# # Create screen
# sc = turtle.Screen()
# sc.title("Pong game")
# sc.bgcolor("white")
# sc.setup(width=1000, height=600)

# # Left paddle
# left_pad = turtle.Turtle()
# left_pad.speed(0)
# left_pad.shape("square")
# left_pad.color("black")
# left_pad.shapesize(stretch_wid=6, stretch_len=2)
# left_pad.penup()
# left_pad.goto(-400, 0)

# # Right paddle
# right_pad = turtle.Turtle()
# right_pad.speed(0)
# right_pad.shape("square")
# right_pad.color("black")
# right_pad.shapesize(stretch_wid=30, stretch_len=2)
# right_pad.penup()
# right_pad.goto(400, 0)

# # Ball of circle shape
# hit_ball = turtle.Turtle()
# hit_ball.speed(40)
# hit_ball.shape("circle")
# hit_ball.color("blue")
# hit_ball.penup()
# hit_ball.goto(0, 0)
# hit_ball.dx = 5
# hit_ball.dy = -5

# # Initialize the score
# left_player = 0
# # right_player = 0

# # Displays the score
# sketch = turtle.Turtle()
# sketch.speed(0)
# sketch.color("blue")
# sketch.penup()
# sketch.hideturtle()
# sketch.goto(0, 260)
# sketch.write("Left_player : 0", align="center", font=("Courier", 24, "normal"))

# # Functions to move paddle vertically
# def mainPaddleMovement(ax):
#     if ax.value < 0.3:
#         paddleaup()
#     if ax.value > -0.3:
#         paddleadown()

# def paddleaup():
# 	y = left_pad.ycor()
# 	y += 20
# 	left_pad.sety(y)

# def paddleadown():
# 	y = left_pad.ycor()
# 	y -= 20
# 	left_pad.sety(y)

# def paddlebup():
# 	y = right_pad.ycor()
# 	y += 20
# 	right_pad.sety(y)

# def paddlebdown():
# 	y = right_pad.ycor()
# 	y -= 20
# 	right_pad.sety(y)

# Keyboard bindings
# sc.listen()
# sc.onkeypress(paddleaup, "w")
# sc.onkeypress(paddleadown, "s")
# sc.onkeypress(paddlebup, "Up")
# sc.onkeypress(paddlebdown, "Down")

# def update_screen():
#     #while True:
#         sc.update()

#         hit_ball.setx(hit_ball.xcor()+hit_ball.dx)
#         hit_ball.sety(hit_ball.ycor()+hit_ball.dy)

#         # Checking borders
#         if hit_ball.ycor() > 280:
#             hit_ball.sety(280)
#             hit_ball.dy *= -1

#         if hit_ball.ycor() < -280:
#             hit_ball.sety(-280)
#             hit_ball.dy *= -1

#         # if hit_ball.xcor() > 500:
#         # 	hit_ball.goto(0, 0)
#         # 	hit_ball.dy *= -1
#         # 	left_player += 1
#         # 	sketch.clear()
#         # 	sketch.write("Left_player : {} Right_player: {}".format(left_player, right_player), align="center", font=("Courier", 24, "normal"))

#         if hit_ball.xcor() < -500:
#             hit_ball.goto(0, 0)
#             hit_ball.dy *= -1
#             # right_player += 1
#             sketch.clear()
#             sketch.write("Left_player : {}".format(left_player), align="center", font=("Courier", 24, "normal"))

#         # Paddle ball collision
#         if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) and (hit_ball.ycor() < right_pad.ycor() + 300 and hit_ball.ycor() > right_pad.ycor() - 300):
#             hit_ball.setx(360)
#             hit_ball.dx *= -1
            
#         if (hit_ball.xcor() < -360 and hit_ball.xcor() > -370) and (hit_ball.ycor() < left_pad.ycor() + 60 and hit_ball.ycor() > left_pad.ycor() - 60):
#             hit_ball.setx(-360)
#             hit_ball.dx *= -1