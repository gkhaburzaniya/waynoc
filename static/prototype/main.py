from pyscript.web import page, div

page["#loading"][0].remove()
main = page["main"][0]

field = div(style={"width": "300px", "height": "300px", "border": "2px solid black"})

main.append(field)
