# sprites.py
import turtle
import config

class Sprite(turtle.Turtle):
    def __init__(self, x, y, shape, color):
        super().__init__()
        self.penup()
        self.speed(0)
        self.shape(shape)
        self.color(color)
        self.goto(x, y)

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, "ino.gif", "#f5e82f") 
        self.shapesize(1.2, 1.2) 
        self.dy = 0 
        
    def flap(self):
        self.dy = config.FLAP_STRENGTH
        self.setheading(20) 
        
    def update(self):
        self.dy -= config.GRAVITY
        self.sety(self.ycor() + self.dy)
        
        if self.dy < 0 and self.heading() > -45:
            self.setheading(self.heading() - 3)
            
        if self.ycor() < -(config.SCREEN_HEIGHT/2) + 20 or self.ycor() > (config.SCREEN_HEIGHT/2):
            return True 
        return False

class Pipe(Sprite):
    def __init__(self, x, y, is_top, cap_y):
        super().__init__(x, y, "square", config.COLOR_PIPE) 
        self.shapesize(stretch_wid=30, stretch_len=3.5) 
        
        self.cap = Sprite(x, cap_y, "square", config.COLOR_PIPE_CAP) 
        self.cap.shapesize(stretch_wid=1.5, stretch_len=4.2) 
        
        self.is_top = is_top
        self.passed = False 
        self.width = 84 
        self.height = 600
        
        # We store the real position in memory instead of using turtle coords
        self.logical_x = x
        self.pipe_y = y
        self.cap_y = cap_y
        
        # Instantly hide the active shapes off-screen so they don't block the text
        self.goto(0, 1000)
        self.cap.goto(0, 1000)
        
    def update(self):
        self.logical_x -= config.PIPE_SPEED
        
        # Erase previous stamps
        self.clear()
        self.cap.clear()
        
        # Go to real position, stamp ink onto the canvas
        self.goto(self.logical_x, self.pipe_y)
        self.stamp()
        
        self.cap.goto(self.logical_x, self.cap_y)
        self.cap.stamp()
        
        # Move active turtles back off-screen
        self.goto(0, 1000)
        self.cap.goto(0, 1000)

    def is_collision(self, player):
        player_radius = 12 
        bx, by = player.xcor(), player.ycor()
        px, py = self.logical_x, self.pipe_y
        
        b_left, b_right = bx - player_radius, bx + player_radius
        b_top, b_bottom = by + player_radius, by - player_radius
        
        p_left, p_right = px - (self.width/2), px + (self.width/2)
        p_top, p_bottom = py + (self.height/2), py - (self.height/2)
        
        if (b_right > p_left and b_left < p_right and b_top > p_bottom and b_bottom < p_top):
            return True
        return False
        
    def hide(self):
        # Clears stamps when pipe is deleted
        self.clear()
        self.cap.clear()

class ScoreBoard(Sprite):
    def __init__(self):
        super().__init__(0, 0, "square", "white")
        self.hideturtle()
        
    def draw_live_score(self, current_score):
        self.clear() # Erase old text
        
        # Draw Title
        self.goto(0, config.SCREEN_HEIGHT/2 - 60)
        self.write("flappINO", align="center", font=("Courier", 32, "bold"))
        
        # Draw Score
        self.goto(0, config.SCREEN_HEIGHT/2 - 130)
        self.write(f"{current_score}", align="center", font=("Courier", 50, "bold"))
        
    def show_game_over(self):
        self.clear()
        self.goto(0, 20)
        self.write("GAME OVER", align="center", font=("Courier", 50, "bold"))
        self.goto(0, -30)
        self.write("Press 'R' to Restart", align="center", font=("Courier", 24, "normal"))