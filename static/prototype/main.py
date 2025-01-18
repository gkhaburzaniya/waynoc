import asyncio
from random import random

from pyscript import when, window
from pyscript.ffi import to_js, create_proxy
from pyscript.web import page, div

page["#loading"][0].remove()
main = page["main"][0]

MOB_SIZE = 15
FIELD_SIZE = 300
BLAST_SIZE = 5

enemies = {}
rate_of_fire = 0.1


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
                "width": f"{MOB_SIZE}px",
                "height": f"{MOB_SIZE}px",
                "position": "absolute",
                "left": "0px",
                "top": f"{FIELD_SIZE - MOB_SIZE}px",
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
        return int(self.element.style["top"][:-2])

    @y.setter
    def y(self, value):
        self.element.style["top"] = str(value) + "px"

    async def move(self):
        move_speed = 5
        self.moving = True
        while (
            self.moving_left or self.moving_right or self.moving_up or self.moving_down
        ):
            if self.moving_right and self.x != (FIELD_SIZE - MOB_SIZE):
                self.x += move_speed
            elif self.moving_left and self.x != 0:
                self.x -= move_speed
            if self.moving_up and self.y != 0:
                self.y -= move_speed
            elif self.moving_down and self.y != (FIELD_SIZE - MOB_SIZE):
                self.y += move_speed
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


player = Player()


async def blast_finish(mana_blast):
    def check_collision(_):
        mana_blast_rect = mana_blast.getBoundingClientRect()
        for num, enemy in enemies.items():
            enemy_rect = enemy.getBoundingClientRect()
            if (
                mana_blast_rect.top < enemy_rect.bottom
                and mana_blast_rect.bottom > enemy_rect.top
                and mana_blast_rect.left < enemy_rect.right
                and mana_blast_rect.right > enemy_rect.left
            ):
                enemy.remove()
                mana_blast.remove()
                del enemies[num]
                return
            elif mana_blast_rect.top == 0:
                return
        else:
            window.requestAnimationFrame(create_proxy(check_collision))

    window.requestAnimationFrame(create_proxy(check_collision))


field = div(
    style={
        "width": f"{FIELD_SIZE}px",
        "height": f"{FIELD_SIZE}px",
        "display": "flex",
        "position": "relative",
        "background-color": "grey",
    }
)


def create_enemy():
    return div(
        style={
            "width": f"{MOB_SIZE}px",
            "height": f"{MOB_SIZE}px",
            "left": f"{random() * (FIELD_SIZE - MOB_SIZE)}px",
            "position": "absolute",
            "background-color": "red",
            "border": "2px solid black",
        }
    )


def kickoff():
    field.append(player.element)
    main.append(field)
    asyncio.create_task(spawn_enemies())


async def spawn_enemies():
    num = 0
    while True:
        await asyncio.sleep(1)
        enemies[num] = create_enemy()
        field.append(enemies[num])
        num += 1


async def blast():
    flytime = player.y / 200  # flytime is in seconds
    mana_blast = div(
        style={
            "width": f"{BLAST_SIZE}px",
            "height": f"{BLAST_SIZE}px",
            "position": "absolute",
            "left": f"{player.x + (MOB_SIZE - BLAST_SIZE)/2}px",
            "top": f"{player.y}px",
            "background-color": "blue",
        }
    )
    field.append(mana_blast)
    mana_blast.animate(
        to_js([{"top": "0px"}]), duration=flytime * 1000, easing="linear"
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


kickoff()
