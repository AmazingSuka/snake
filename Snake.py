import tkinter as tk
import random as rnd

#Constants
WIDTH = 600
HEIGHT = 600
BG_COLOR = 'black'
SIZE_R = 20
SNAKE_COLOR = 'white'
BODY_SIZE = 4
SNAKE_START_POSITION_X = WIDTH / 2
SNAKE_START_POSITION_Y = HEIGHT / 2
SPEED = 100
LEFT = 37
RIGHT = 39
UP = 38
DOWN = 40
#
eats = []
body = []    
#Snake piece
class Piece():
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
        
    def draw(self): #draw snake element
        canvas.create_rectangle(self.x, self.y, self.x + SIZE_R, self.y + SIZE_R, fill=self.color)
    
    def hide(self): #hide snake element
        canvas.create_rectangle(self.x, self.y, self.x + SIZE_R, self.y + SIZE_R, fill=BG_COLOR)

#SNAKE
class Snake():
    current_direction = 37
    score = 0
    #draw started snake
    def create_start_snake(self,body_list):
        x = SNAKE_START_POSITION_X
        if len(body_list) <= BODY_SIZE:
            for i in range(BODY_SIZE): # create BODY_SIZE(4) elements
                if check_network_coordinate(x, SNAKE_START_POSITION_Y):
                    body_list.append(Piece(x, SNAKE_START_POSITION_Y, SIZE_R, SNAKE_COLOR)) # create element
                    body_list[i].draw() # draw element
                    x+= SIZE_R # change coordinate X for next element
                    
    def is_colision_with_eat(self, eats, head):
        a = head.getX() - eats[0].getX()
        b = head.getY() - eats[0].getY()
        return (a**2 + b**2)**0.5 < SIZE_R 
    
    def is_colision_with_self(self, head, body):
        for elem in body[3:]:
            if head.getX() == elem.getX() and head.getY() == elem.getY():
                return True
            elif head.getX() == elem.getX() and head.getY() + SIZE_R  == elem.getY() + SIZE_R:
                return True
                
    #snake trafic
    def move(self, *args, **kwargs):
        x = body[0].getX() # Head Coordinates
        y = body[0].getY() # Head Coordinates
        if check_network_coordinate(x, y):
            if self.current_direction == LEFT:
                body.insert(0, Piece(x - SIZE_R, y, SIZE_R, SNAKE_COLOR)) # Create New Head
            elif self.current_direction == RIGHT:
                body.insert(0, Piece(x + SIZE_R, y, SIZE_R, SNAKE_COLOR))
            elif self.current_direction == UP:
                body.insert(0, Piece(x, y - SIZE_R, SIZE_R, SNAKE_COLOR))
            elif self.current_direction == DOWN:
                body.insert(0, Piece(x, y + SIZE_R, SIZE_R, SNAKE_COLOR))
        # colision with wall
        if x < 0:   #left wall
            body[0].setX(WIDTH)
        elif x > WIDTH: #right wall
            body[0].setX(0)
        elif y < 0:  # up wall
            body[0].setY(HEIGHT) 
        elif y > HEIGHT: # down wall
            body[0].setY(0)
        
        if self.is_colision_with_eat(eats, body[0]):
            snake.eating()
            canvas.create_rectangle(15,15,45,45 , fill = BG_COLOR)
            self.score +=1
            body[0].draw()
        else:
            body[0].draw()
            body[-1].hide() # hide tail
            body.remove(body[-1]) # delete tail
            
            
    def eating(self, *args, **kwargs):
        eats[0].hide()
        eats.remove(eats[0])
        create_eat(eats)
        
#remember press key code
def key_code(event):
    if snake.current_direction % 2 == 0 and event.keycode % 2 == 0:
        return
    elif snake.current_direction % 2 != 0 and event.keycode % 2 != 0:
        return
    else:
        snake.current_direction = event.keycode
        
# Create eat on the form
def create_eat(eat):
    x = rnd.randint(SIZE_R, WIDTH - SIZE_R)
    y = rnd.randint(SIZE_R, HEIGHT - SIZE_R)
    if check_network_coordinate(x, y):
        eat.append(Piece(x, y, SIZE_R, SNAKE_COLOR))
        eat[0].draw()
    else: return create_eat(eat)
        
# check rectangles coordinateo
def check_network_coordinate(x, y):
    return x % 20 == 0 and y % 20 == 0
    
#main 
def main(): 
    if snake.is_colision_with_self(body[0], body):
        canvas.create_text(SNAKE_START_POSITION_X,SNAKE_START_POSITION_Y, 
                           text="YOU LOSE", font="Arial 50", fill='red')
    else:
        snake.move()
        canvas.create_text(30,30, text=snake.score, font="Arial", fill=SNAKE_COLOR)
        root.after(SPEED, main)
        
        
        
root = tk.Tk()
root.title('Snake')
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR) # Create form
canvas.pack()
snake = Snake()
snake.create_start_snake(body)
frame = tk.Frame(root, width=WIDTH, height=HEIGHT)
frame.bind('<Left>', key_code)
frame.bind('<Right>', key_code)
frame.bind('<Up>', key_code)
frame.bind('<Down>', key_code)
frame.focus_set()
frame.pack()
create_eat(eats)
main()
root.mainloop()