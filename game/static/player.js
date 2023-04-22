class Player{
    constructor() {
        this.name = "";
        this.int = 0;
        this.dex = 0;
        this.str = 0;
        this.end = 0;
        this.age = 0;
    }

    change(attr, change) {
        if (change > 0) {
            return "+" + change + " " + attr;
        } else if (change < 0) {
            return change + " " + attr;
        }
    }
    change_int(change) {
        this.int = this.int + change;
        return this.change("Int", change);
    }
    change_dex(change) {
        this.dex = this.dex + change;
        return this.change("Dex", change);
    }
    change_str(change) {
        this.str = this.str + change;
        return this.change("Str", change);
    }
    change_end(change) {
        this.end = this.end + change;
        return this.change("End", change);
    }
    change_name(new_name) {
        this.name = new_name;
        return "Your name is " + new_name;
    }
}

player = new Player();
function nextSeason() {
    let event_list = [];
    let final_text = "<b>"
    event_list.push(player.change_str(1));
    event_list.push(player.change_dex(1));
    event_list.push(player.change_int(1));
    event_list.push(player.change_end(1));
    player.age += 1/4;
    document.getElementById("str").innerHTML = player.str;
    document.getElementById("dex").innerHTML = player.dex;
    document.getElementById("int").innerHTML = player.int;
    document.getElementById("end").innerHTML = player.end;
    document.getElementById("age").innerHTML = player.age;
    event_list.forEach((event) => final_text = final_text + event + "<br>");
    final_text += "</b>"
    document.getElementById("effect_text").innerHTML = final_text;
}
