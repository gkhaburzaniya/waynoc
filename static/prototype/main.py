import asyncio
from random import random

from pyscript import when, window
from pyscript.web import page, div
from pyscript.ffi import to_js

from player import player
from shared import MOB_SIZE, FIELD_SIZE, enemies

page["#loading"][0].remove()
main = page["main"][0]

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
            "top": "0px",
            "left": f"{random() * (FIELD_SIZE - MOB_SIZE)}px",
            "position": "absolute",
            "background-color": "red",
            "border": "2px solid black",
        }
    )


def kickoff():
    main.append(player.xp_div)
    field.append(player.element)
    main.append(field)
    main.append(div(player.mental_button))
    asyncio.create_task(spawn_enemies())


async def spawn_enemies():
    num = 0
    while True:
        await asyncio.sleep(1)
        player.xp += 1
        enemy = create_enemy()
        enemies[num] = enemy
        field.append(enemy)
        enemy.animate(
            to_js([{"top": "0px"}, {"top": "100px"}]), duration=3000, easing="linear",
            fill="forwards",
        )
        num += 1


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
