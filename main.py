import tkinter as tk
import tkinter.font as tkFont


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notor")
        self.text = ""

        self.canvas_manager = CanvasManager(self.root)
        self.cursor_manager = CursorManager(self.canvas_manager, self)

        self.root.bind("<space>", self.on_space_pressed)
        self.root.bind("<BackSpace>", self.on_backspace_pressed)
        self.root.bind("<Return>", self.on_return_pressed)
        self.root.bind("<KeyPress>", self.on_keydown)
        self.root.bind("<Escape>", self.on_escape)
        self.root.bind("<Tab>", self.on_tab)

        self.root.mainloop()
    
    def character_width(event=None,character=None):
        font = tkFont.Font(font='times')
        width = font.measure(character)
        return width 

    def on_tab(self, event):
        self.text += " "
        self.cursor_manager.cursor_increase(distance=self.character_width(" "))
        self.cursor_manager.draw_cursor()
    
    def on_space_pressed(self, event):

        self.text += " "
        self.cursor_manager.cursor_increase(distance=self.character_width(" "))
        self.cursor_manager.draw_cursor()
    
    def on_backspace_pressed(self, event):
        try:
            removed_character = self.text[-1]
        except:
            print("Nothing to remove")
            return
        self.text = self.text[0:-1]
        self.cursor_manager.draw_character(self.text, backspace=True, width=self.character_width(character=removed_character))
        self.cursor_manager.draw_cursor()
    
    def on_return_pressed(self, event):
        self.text += "\n"
        self.cursor_manager.cursor_next_line()
        self.cursor_manager.draw_cursor(return_pressed=True)

    def on_keydown(self, event):

        if(event.keycode == 16):
            return
        print(event.keycode)
        self.text += f"{event.char}"
        self.cursor_manager.draw_character(self.text,backspace=False,width=self.character_width(event.char))

    def on_escape(self, event):
        self.root.destroy()


class CanvasManager: 
    def __init__(self, root):
        self.canv_x = 400
        self.canv_y = 400
        self.canv = tk.Canvas(root, width=self.canv_x,height=self.canv_y,cursor='man')
        self.canv.pack()

    def get_canvas(self):
        return self.canv 

class CursorManager:
    def __init__(self, canvas_manager, app):
        self.canv = canvas_manager.get_canvas()
        self.app = app
        self.lines = []
        self.current_line = 0
        self.cursor_line_height = 16
        self.cursor_origin = 5.5
        self.cursor_max = 388
        self.cursor_min = 0
        self.cursor_jump_x = 5
        self.cursor_jump_y = 19.1
        self.cursor_x = self.cursor_origin
        self.cursor_y = self.cursor_origin
        
        self.draw_cursor()

    def draw_cursor(self, return_pressed=None):
        self.canv.delete("cursor")
        if(return_pressed):
            self.cursor_x = self.cursor_origin
        self.canv.create_line(self.cursor_x, self.cursor_y, self.cursor_x, self.cursor_y + self.cursor_line_height, tags="cursor")


    def draw_character(self,char, backspace=None, width=None):
        self.canv.delete("text")
        self.canv.create_text(self.cursor_origin, self.cursor_origin,anchor= tk.NW, justify=tk.LEFT, width=385, font='times',text=char, tags="text", )
        if(not backspace):
            self.cursor_increase(width)
        else:
            self.cursor_decrease(width)
        self.draw_cursor()


    def cursor_increase(self,distance=None):
        self.cursor_x += int(distance)
        if self.cursor_x > self.cursor_max:
            if self.cursor_y < self.cursor_max:
                self.cursor_next_line()
            self.cursor_x = self.cursor_origin
        
    def cursor_decrease(self,distance=None):
        self.cursor_x -= int(distance) 
        if self.cursor_x < self.cursor_min:
            if self.cursor_y > self.cursor_min or self.cursor_y > self.cursor_max:
                self.cursor_y -= self.cursor_jump_y
                self.current_line -= 1
                self.cursor_x = self.old_line_width(self.app.text, self.current_line) + self.cursor_origin
            self.cursor_x = self.cursor_x
        
    def cursor_next_line(self):
        if self.cursor_y < self.cursor_max:
            self.cursor_y += self.cursor_jump_y
            self.current_line += 1

    # function to handle backspacing into incomplete lines
    def old_line_width(self,text,line):
        count = 0
        total_width = 0
        line_text = []

        # go through each line until a count == line
        for letter in text:
            if count == line:
                line_text.append(letter)
            if letter == '\n':
                count += 1
        
        for c in line_text:
            total_width += self.app.character_width(c)
        
        return total_width

        
        
if __name__ == "__main__":
    app = Application()


# to do:
# if you hold space bar after next line it gets super funky buggy
# fix last line shenanigans
# cursor movement
# mouse click to move cursor
# add save
# add load
# add character count
# word count
# emoji conversion?