from pyscript.web import page, div
import asyncio
from pyscript import when, window

page["#loading"][0].remove()
main = page["main"][0]


class Player:
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    moving = False
    y = 0

    def __init__(self):
        self.element = div(
            style={
                "width": "5%",
                "height": "5%",
                "position": "absolute",
                "left": "0%",
                "bottom": "0%",
                "background-color": "blue",
                "border": "2px solid black",
                "transition": "0.05s linear",
            }
        )

    @property
    def x(self):
        return int(self.element.style["left"][:-1])

    @x.setter
    def x(self, value):
        self.element.style["left"] = str(value) + "%"

    async def move(self):
        move_speed = 2
        self.moving = True
        while (
            self.moving_left or self.moving_right or self.moving_up or self.moving_down
        ):
            if self.moving_right and self.x != 100:
                self.x = self.x + move_speed
            elif self.moving_left and self.x != 0:
                self.x = self.x - move_speed
            if self.moving_up and self.y != 100:
                self.y += move_speed
                self.element.style["bottom"] = str(self.y) + "%"
            if self.moving_down and self.y != 0:
                self.y -= move_speed
                self.element.style["bottom"] = str(self.y) + "%"
            await asyncio.sleep(0.05)
        self.moving = False


field = div(
    style={
        "width": "300px",
        "height": "300px",
        "display": "flex",
        "position": "relative",
        "background-color": "grey",
        "border": "2px solid black",
    }
)
enemy = div(
    style={
        "width": "5%",
        "height": "5%",
        "background-color": "red",
        "border": "2px solid black",
    }
)
player = Player()
field.append(enemy)
field.append(player.element)
main.append(field)


@when("keydown", window)
def keydown(event):
    if event.key == "ArrowUp":
        player.moving_up = True
    elif event.key == "ArrowDown":
        player.moving_down = True
    elif event.key == "ArrowLeft":
        player.moving_left = True
    elif event.key == "ArrowRight":
        player.moving_right = True
    if not player.moving:
        asyncio.create_task(player.move())


@when("keyup", window)
def keyup(event):
    if event.key == "ArrowUp":
        player.moving_up = False
    elif event.key == "ArrowDown":
        player.moving_down = False
    elif event.key in "ArrowLeft":
        player.moving_left = False
    elif event.key in "ArrowRight":
        player.moving_right = False
