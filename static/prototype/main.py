from pyscript.web import page, div
import asyncio
from pyscript import when, window

page["#loading"][0].remove()
main = page["main"][0]


class Player:
    def __init__(self):
        self.element = div(style={"width": "50px", "height": "50px",
                                  "position": "absolute",
                                  "bottom": "0%",
                                  "background-color": "blue",
                                  "border": "2px solid black",
                                  "transition": "0.05s linear"})
        self.x = 0
        self.y = 0

    async def move(self, x=0, y=0):
        while moving:
            self.x += x
            self.y += y
            self.element.style["left"] = str(self.x) + "%"
            self.element.style["bottom"] = str(self.y) + "%"
            await asyncio.sleep(0.05)


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


# TODO make first movement not take significantly longer
# TODO make movement bound by field
@when("keydown", window)
def keydown(event):
    global moving
    moving = True
    if event.key == "ArrowUp":
        asyncio.ensure_future(player.move(y=5))
    elif event.key == "ArrowDown":
        asyncio.ensure_future(player.move(y=-5))
    elif event.key == "ArrowLeft":
        asyncio.ensure_future(player.move(x=-5))
    elif event.key == "ArrowRight":
        asyncio.ensure_future(player.move(x=5))


@when("keyup", window)
def keyup(_):
    global moving
    moving = False
