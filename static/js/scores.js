window.onload = function() {
    var roles = document.getElementsByClassName("td-role");
    for (var i=0; i<roles.length; i++){
        var cards = roles[i].innerText.split("-")
        while (roles[i].firstChild) {
            roles[i].removeChild(roles[i].firstChild);
        }
        for (var j=0; j< cards.length; j++){
            var roleNode = document.createElement("DIV"); 
            roleNode.className= "card sprite " + cards[j];
            roleNode.setAttribute("data-toggle", "tooltip");
            switch(cards[j]) {
                case "bluedigger":
                    roleNode.setAttribute("title", "Blue Team Digger.");
                break;
                case "greendigger":
                    roleNode.setAttribute("title", "Green Team Digger.");
                break;
                case "profiteer":
                    roleNode.setAttribute("title", "The Profiteer.");
                break;
                case "geologist":
                    roleNode.setAttribute("title", "The Geologist.");
                break;
                case "theboss":
                    roleNode.setAttribute("title", "The Boss.");
                break;
                case "saboteurs":
                    roleNode.setAttribute("title", "The Saboteur.");
                break;
        }
        roles[i].appendChild(roleNode);
        $('[data-toggle="tooltip"]').tooltip();
        }
    }
};