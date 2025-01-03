from pyscript.web import page, div

page["#loading"][0].remove()
main = page["main"][0]

field = div(style={"width": "300px", "height": "300px",
                   "background-color": "grey",
                   "border": "2px solid black"})
player = div(style={"width": "50px", "height": "50px",
                    "background-color": "blue",
                    "border": "2px solid black"})

field.append(player)
main.append(field)
