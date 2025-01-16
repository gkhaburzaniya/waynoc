import asyncio

from pyscript import when, window
from pyscript.ffi import to_js, create_proxy
from pyscript.web import page, div

page["#loading"][0].remove()
main = page["main"][0]


class Player:
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    moving = False
    start_firing = False
    firing = False

    def __init__(self):
        self.element = div(
            style={
                "width": "15px",
                "height": "15px",
                "position": "absolute",
                "left": "0px",
                "bottom": "0px",
                "background-color": "green",
                "border": "2px solid black",
                "transition": "0.05s linear",
            }
        )

    @property
    def x(self):
        return int(self.element.style["left"][:-2])

    @x.setter
    def x(self, value):
        self.element.style["left"] = str(value) + "px"

    @property
    def y(self):
        return int(self.element.style["bottom"][:-2])

    @y.setter
    def y(self, value):
        self.element.style["bottom"] = str(value) + "px"

    @property
    def width(self):
        return int(self.element.style["width"][:-2])

    @property
    def height(self):
        return int(self.element.style["height"][:-2])

    async def move(self):
        move_speed = 5
        self.moving = True
        while (
            self.moving_left or self.moving_right or self.moving_up or self.moving_down
        ):
            if self.moving_right and self.x != (295 - self.width):
                self.x += move_speed
            elif self.moving_left and self.x != 0:
                self.x -= move_speed
            if self.moving_up and self.y != (295 - self.height):
                self.y += move_speed
            if self.moving_down and self.y != 0:
                self.y -= move_speed
            await asyncio.sleep(0.05)
        self.moving = False

    async def fire(self):
        self.firing = True
        blasts = set()
        while self.start_firing:
            mana_blast = await blast()
            blasts.add(asyncio.create_task(blast_finish(mana_blast)))

        self.firing = False

        for blast_task in blasts:
            await blast_task


async def blast_finish(mana_blast):
    def check_collision(_):
        mana_blast_rect = mana_blast.getBoundingClientRect()
        enemy_rect = enemy.getBoundingClientRect()
        if (
            mana_blast_rect.top < enemy_rect.bottom
            and mana_blast_rect.bottom > enemy_rect.top
            and mana_blast_rect.left < enemy_rect.right
            and mana_blast_rect.right > enemy_rect.left
        ):
            enemy.remove()
            mana_blast.remove()
        else:
            window.requestAnimationFrame(create_proxy(check_collision))

    window.requestAnimationFrame(create_proxy(check_collision))


field = div(
    style={
        "width": "305px",
        "height": "305px",
        "display": "flex",
        "position": "relative",
        "background-color": "grey",
        "border": "5px solid black",
    }
)
enemy = div(
    style={
        "width": "15px",
        "height": "15px",
        "background-color": "red",
        "border": "2px solid black",
    }
)
player = Player()
field.append(enemy)
field.append(player.element)
main.append(field)

rate_of_fire = 0.1


async def blast():
    flytime = (300 - player.y) / 200  # flytime is in seconds
    mana_blast = div(
        style={
            "width": "5px",
            "height": "5px",
            "position": "absolute",
            "left": f"{player.x}px",
            "bottom": f"{player.y}px",
            "background-color": "blue",
        }
    )
    field.append(mana_blast)
    mana_blast.animate(
        to_js([{"bottom": "300px"}]), duration=flytime * 1000, easing="linear"
    ).onfinish = lambda _: mana_blast.remove()
    await asyncio.sleep(rate_of_fire)  # Hangs if there's no sleep.
    return mana_blast


@when("keydown", window)
def keydown(event):
    if event.code == "ArrowUp":
        player.moving_up = True
    elif event.code == "ArrowDown":
        player.moving_down = True
    elif event.code == "ArrowLeft":
        player.moving_left = True
    elif event.code == "ArrowRight":
        player.moving_right = True
    elif event.code == "Space":
        player.start_firing = True
    if not player.moving:
        asyncio.create_task(player.move())
    if not player.firing:
        asyncio.create_task(player.fire())


@when("keyup", window)
def keyup(event):
    if event.code == "ArrowUp":
        player.moving_up = False
    elif event.code == "ArrowDown":
        player.moving_down = False
    elif event.code in "ArrowLeft":
        player.moving_left = False
    elif event.code in "ArrowRight":
        player.moving_right = False
    elif event.code in "Space":
        player.start_firing = False
