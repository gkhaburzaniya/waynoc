import asyncio

from shared import FIELD_SIZE, MOB_SIZE, BLAST_SIZE, enemies

from pyscript import window
from pyscript.web import div, button
from pyscript.ffi import to_js, create_proxy


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
        self.mental_button = button(
            "Mental 1",
            type="submit",
            classes=["btn", "btn-secondary"],
            onclick=self.mental_up,
        )

    @property
    def mental(self):
        # "Mental 1" turns into 1
        return int(self.mental_button.textContent.split()[1])

    @mental.setter
    def mental(self, value):
        self.mental_button.textContent = "Mental " + str(value)

    @property
    def rate_of_fire(self):
        return 0.05 + 2 / self.mental

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

    def mental_up(self, _):
        self.mental += 1

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
            mana_blast = await self.blast()
            blasts.add(asyncio.create_task(self.blast_finish(mana_blast)))
            await asyncio.sleep(self.rate_of_fire)

        self.firing = False

        for blast_task in blasts:
            await blast_task

    async def blast(self):
        flytime = self.y / 200  # flytime is in seconds
        field = self.element.parent
        mana_blast = div(
            style={
                "width": f"{BLAST_SIZE}px",
                "height": f"{BLAST_SIZE}px",
                "position": "absolute",
                "left": f"{player.x + (MOB_SIZE - BLAST_SIZE) / 2}px",
                "top": f"{player.y}px",
                "background-color": "blue",
            }
        )
        field.append(mana_blast)
        mana_blast.animate(
            to_js([{"top": "0px"}]), duration=flytime * 1000, easing="linear"
        ).onfinish = lambda _: mana_blast.remove()
        return mana_blast

    @staticmethod
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


player = Player()
