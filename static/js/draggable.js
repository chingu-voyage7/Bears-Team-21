
function dragElement(elmnt) {
    var nodeDrag = document.getElementById("drag-chat")
    nodeDrag.onmousedown = dragMouseDown;
    var offX = nodeDrag.offsetWidth / 2;
    var offY  = nodeDrag.offsetHeight / 2;

    function dragMouseDown(e) {
      e = e || window.event;
      e.preventDefault();
      document.onmouseup = closeDragElement;
      document.onmousemove = elementDrag;
    }
    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      offsetx = 
      elmnt.style.top =( e.clientY -offY) + "px";
      elmnt.style.left =( e.clientX - offX) + "px";
    }
    function closeDragElement() {
      document.onmouseup = null;
      document.onmousemove = null;
    }
}