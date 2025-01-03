from pyscript.web import page, div

page["#loading"][0].remove()
main = page["main"][0]

field = div(style={"width": "300px", "height": "300px",
                   "display": "flex",
                   "position": "relative",
                   "background-color": "grey",
                   "border": "2px solid black"})
player = div(style={"width": "50px", "height": "50px",
                    "position": "absolute",
                    "bottom": "0px",
                    "background-color": "blue",
                    "border": "2px solid black"})
enemy = div(style={"width": "50px", "height": "50px",
                   "background-color": "red",
                   "border": "2px solid black"})

field.append(enemy)
field.append(player)
main.append(field)
