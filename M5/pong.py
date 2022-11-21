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

class Pong:
    def __init__(self, gx1, gx2):
        self.lp_moveup = True
        self.rp_moveup = True
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
        self.right_pad.shapesize(stretch_wid=6, stretch_len=2)
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
        self.left_player = 0
        self.right_player = 0

        # Displays the score
        self.sketch = turtle.Turtle()
        self.sketch.speed(0)
        self.sketch.color("blue")
        self.sketch.penup()
        self.sketch.hideturtle()
        self.sketch.goto(0, 260)
        self.sketch.write("Left_player : {} Right_player: {}".format(self.left_player, self.right_player), align="center", font=("Courier", 24, "normal"))

        self.update_screen(gx1, gx2)

    # Functions to move paddle vertically
    def leftPaddleMovement(self, gx1):
        if gx1.value < -200.0:
            self.lp_moveup = True
        if gx1.value > 200.0:
            self.lp_moveup = False

        if self.lp_moveup:
            self.paddleaup()
        else:
            self.paddleadown()
    
    def rightPaddleMovement(self, gx2):
        if gx2.value < -200.0:
            self.rp_moveup = True
        if gx2.value > 200.0:
            self.rp_moveup = False

        if self.rp_moveup:
            self.paddlebup()
        else:
            self.paddlebdown()

    def paddleaup(self):
        y = self.left_pad.ycor()
        if y < 300:
            y += 10
            self.left_pad.sety(y)

    def paddleadown(self):
        y = self.left_pad.ycor()
        if y > -300:
            y -= 10
            self.left_pad.sety(y)
    
    def paddlebup(self):
        y = self.right_pad.ycor()
        if y < 300:
            y += 20
            self.right_pad.sety(y)

    def paddlebdown(self):
        y = self.right_pad.ycor()
        if y > -300:
            y -= 20
            self.right_pad.sety(y)
    
    def update_screen(self, gx1, gx2):
        while True:
            self.sc.update()
            self.leftPaddleMovement(gx1)
            self.rightPaddleMovement(gx2)

            self.hit_ball.setx(self.hit_ball.xcor()+self.hit_ball.dx)
            self.hit_ball.sety(self.hit_ball.ycor()+self.hit_ball.dy)

            # Checking borders
            if self.hit_ball.ycor() > 280:
                self.hit_ball.sety(280)
                self.hit_ball.dy *= -1

            if self.hit_ball.ycor() < -280:
                self.hit_ball.sety(-280)
                self.hit_ball.dy *= -1

            if self.hit_ball.xcor() > 500:
                self.hit_ball.goto(0, 0)
                self.hit_ball.dy *= -1
                self.left_player += 1
                self.sketch.clear()
                self.sketch.write("Left_player : {} Right_player: {}".format(self.left_player, self.right_player), align="center", font=("Courier", 24, "normal"))

            if self.hit_ball.xcor() < -500:
                self.hit_ball.goto(0, 0)
                self.hit_ball.dy *= -1
                self.right_player += 1
                self.sketch.clear()
                self.sketch.write("Left_player : {} Right_player: {}".format(self.left_player, self.right_player), align="center", font=("Courier", 24, "normal"))

            # Paddle ball collision
            if (self.hit_ball.xcor() > 360 and self.hit_ball.xcor() < 370) and (self.hit_ball.ycor() < self.right_pad.ycor() + 60 and self.hit_ball.ycor() > self.right_pad.ycor() - 60):
                self.hit_ball.setx(360)
                self.hit_ball.dx *= -1
                
            if (self.hit_ball.xcor() < -360 and self.hit_ball.xcor() > -370) and (self.hit_ball.ycor() < self.left_pad.ycor() + 60 and self.hit_ball.ycor() > self.left_pad.ycor() - 60):
                self.hit_ball.setx(-360)
                self.hit_ball.dx *= -1

