import tkinter as tk

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notor")

        self.canvas_manager = CanvasManager(self.root)
        self.cursor_manager = CursorManager(self.canvas_manager)

        self.root.bind("<space>", self.on_space_pressed)
        self.root.bind("<BackSpace>", self.on_backspace_pressed)
        self.root.bind("<Return>", self.on_return_pressed)
        self.root.bind("<KeyPress>", self.on_keydown)

        self.root.mainloop()
    
    def on_space_pressed(self, event):
        self.cursor_manager.cursor_increase()
        self.cursor_manager.draw_cursor()
    
    def on_backspace_pressed(self, event):
        self.cursor_manager.cursor_decrease()
        self.cursor_manager.draw_cursor()
    
    def on_return_pressed(self, event):
        self.cursor_manager.cursor_next_line()
        self.cursor_manager.draw_cursor()

    def on_keydown(self, event):
        self.cursor_manager.draw_character(event.char)

class CanvasManager:
    def __init__(self, root):
        self.canv_x = 400
        self.canv_y = 400
        self.canv = tk.Canvas(root, width=self.canv_x,height=self.canv_y,cursor='man')
        self.canv.pack()

    def get_canvas(self):
        return self.canv 

class CursorManager:
    def __init__(self, canvas_manager):
        self.canv = canvas_manager.get_canvas()
        self.cursor_line_height = 20
        self.cursor_origin = 10
        self.cursor_max = 385
        self.cursor_min = 20
        self.cursor_jump_x = 5
        self.cursor_jump_y = 18
        self.cursor_x = self.cursor_origin
        self.cursor_y = self.cursor_origin
        
        self.draw_cursor()

    def draw_cursor(self):
        self.canv.delete("cursor")
        self.canv.create_line(self.cursor_x, self.cursor_y, self.cursor_x, self.cursor_y + self.cursor_line_height, tags="cursor")

    def draw_character(self,char):
        self.canv.create_text(self.cursor_x + self.cursor_origin,self.cursor_y + self.cursor_origin, text=char)
        self.cursor_increase()
        self.draw_cursor()

    def cursor_increase(self):
        self.cursor_x += self.cursor_jump_x
        if self.cursor_x > self.cursor_max:
            if self.cursor_y < self.cursor_max:
                self.cursor_y += self.cursor_jump_y
            self.cursor_x = self.cursor_origin
        
    def cursor_decrease(self):
        self.cursor_x -= self.cursor_jump_x
        if self.cursor_x < self.cursor_min:
            if self.cursor_y > self.cursor_min or self.cursor_y > self.cursor_max:
                self.cursor_y -= self.cursor_jump_y
            self.cursor_x = self.cursor_origin
        
    def cursor_next_line(self):
        if self.cursor_y < self.cursor_max:
            self.cursor_y += self.cursor_jump_y

        
if __name__ == "__main__":
    app = Application()
