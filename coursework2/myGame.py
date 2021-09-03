import tkinter as tk
from tkinter import ttk
from random import randint

#Instructions:
# Press c for cheat-code (increases score by 1)
# Press space for pause
# Press b for boss-key


movevalue = 20
mps = 15  
#Pace of game increases on increase of mps
speed = 1000 // mps
pause_text = " "
run = False


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", 
        highlightthickness=0)
 
        #Positions of snake body and food
        self.snakepos = [(100, 100), (80, 100), (60, 100)]  
        self.foodpos = self.set_new_food_position()
        self.direction = "Right"

        self.score = 0   #Score counter
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()
        self.create_objects()

        self.pack()

        self.after(speed, self.perform_actions)


    def load_assets(self):   #Loads all the images required for the game
        self.bodyimage = tk.PhotoImage(file="snake.png")
        self.foodimage = tk.PhotoImage(file="food2.png")
        self.bosskeyphoto = tk.PhotoImage(file="verynice2.png")


    def create_objects(self):   #Creating the body and food objects 
        self.create_text(100, 12, text=f"Score: {self.score} (Speed: {mps})",
        tag="score", fill="#39FF14", font=("Courier", 14, "bold"))

        for x_position, y_position in self.snakepos:
            self.create_image(
                x_position, y_position, image=self.bodyimage, tag="snake"
            )

        self.create_image(*self.foodpos, image=self.foodimage, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="red")   #Sets boundaries

    def check_collisions(self): #Checks for collisions on boundaries of the game
        head_x_position, head_y_position = self.snakepos[0]

        return (
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snakepos[1:])
        

    def check_food_collision(self):  #Checks for collision
        if self.snakepos[0] == self.foodpos:
            self.score += 1
            self.snakepos.append(self.snakepos[-1])

            if(self.score) % 5 == 0:
                global mps
                mps=mps+1

            self.create_image(*self.snakepos[-1], image=self.bodyimage,
            tag="snake")
            self.foodpos = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.foodpos)
            score = self.find_withtag("score")
            self.itemconfigure(score,
            text=f"Score: {self.score} (Speed: {mps})", tag="score")
            

    def end_game(self):  #End screen for game after snake collides with boundary
        self.delete(tk.ALL)
        f = open("test1.txt", "a")
        f.write(user_name +  "," + str(self.score) + "\n")
        f.close()

        scoreboard = []
        for line in open("test1.txt"):
            scoreboard.append(line)

        sorted_scores = sorted(scoreboard, key= lambda x: x[1], reverse=True)
        # Sorts score in the array in decreasing order of scores  

        self.create_text(self.winfo_width()/2, 100, 
        text=f"Game Over. You scored {self.score}!",
        fill="#39FF14", font=("courier", 14, "bold"))
        self.create_text(self.winfo_width()/2, 200, 
        text="Leaderboard", fill="white", font=("courier", 14, "bold"))
        self.create_text(self.winfo_width()/2, 300, 
        text=sorted_scores, fill="#39FF14", font=("courier", 14, "bold"))

        print(sorted_scores) 

        
    def move_snake(self):  #Sets head positions when the snake moves
        head_x_position, head_y_position = self.snakepos[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - movevalue, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + movevalue, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + movevalue)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - movevalue)

        self.snakepos = [new_head_position] + self.snakepos[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snakepos):
            self.coords(segment, position)

    def on_key_press(self, e):  #Assigns keybinds for controlling aspects of the game
        keypress = e.keysym

        all_directions = ("Up", "Down", "Left", "Right") 
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            keypress in all_directions
            and {keypress, self.direction} not in opposites
        ):
            self.direction = keypress  #Controls movement of snake

        if keypress == "b":  #Controls bosskey
            self.create_image(self.winfo_width()/2, self.winfo_height()/2, 
            image=self.bosskeyphoto, tag="verynice") 
        
        if keypress == "c":  #Controls cheatkey
            self.score+=1
            self.snakepos.append(self.snakepos[-1])
            if(self.score) % 5 == 0:
                global mps
                mps=mps+1

            score = self.find_withtag("score")

            self.itemconfigure(score, text=f"Score: {self.score} (Speed: {mps})", 
            tag="score")

        if keypress == "space":  #Controls
            global run, pause_text 
            if run == False:
                run = True
                self.delete(pause_text)
                self.after(speed, self.perform_actions)
            else:
                run = False
                pause_text = self.create_text(302,250, 
                font=("TkDefaultFont", 14), text="Press space to resume.", fill="white")  


    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()
        self.move_snake()

        self.after(speed, self.perform_actions)


    def set_new_food_position(self):  #Sets new position for the food
        while True:
            x_position = randint(1, 29) * movevalue
            y_position = randint(3, 30) * movevalue
            food_position = (x_position, y_position)

            if food_position not in self.snakepos:
                return food_position


def myClick():
    global user_name
    user_name = name_entry.get()
    window.destroy()  #Destroys current widgets to start the main-game
    Snake()


def mainmenu():
    style = tk.ttk.Style()
    style.configure('TEntry', foreground="green")  
    global name_entry
    
    name_entry = tk.ttk.Entry(window, width=25, justify="center",
    font=("courier", 14, "bold"))
    #  Creates text-box to enter game

    name_entry.focus_force()
    name_entry.place(relx=0.5, rely=0.5, anchor="center")

    button = tk.Button(window, text="Start game!", fg="black",
    bg="green", command=myClick)
    button.pack(side="bottom", pady=250)
    #  Creates the button to start game

      
window = tk.Tk()
window.title("Python wants pizza")
window.geometry("600x620")
window.configure(background="black")
icon = tk.PhotoImage(file= "Snake-icon.png")
window.iconphoto(False, icon)
window.resizable(False, False)
mainmenu()
window.mainloop()