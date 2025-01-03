from pyscript.web import page, div
from pyscript import when, window

page["#loading"][0].remove()
main = page["main"][0]


class Player:
    def __init__(self):
        self.element = div(style={"width": "50px", "height": "50px",
                                  "position": "absolute",
                                  "bottom": "0%",
                                  "background-color": "blue",
                                  "border": "2px solid black"})
        self.x = 0
        self.y = 0

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        self.element.style["bottom"] = str(self.x) + "%"
        self.element.style["left"] = str(self.y) + "%"


field = div(style={"width": "300px", "height": "300px",
                   "display": "flex",
                   "position": "relative",
                   "background-color": "grey",
                   "border": "2px solid black"})
enemy = div(style={"width": "50px", "height": "50px",
                   "background-color": "red",
                   "border": "2px solid black"})
player = Player()
field.append(enemy)
field.append(player.element)
main.append(field)


@when("keydown", window)
def move(event):
    if event.key == "ArrowUp":
        player.move(x=5)
