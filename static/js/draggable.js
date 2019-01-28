
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


//document.getElementById('chat').addEventListener('mousedown', initialiseResize, false);

function initialiseResize(e) {
	window.addEventListener('mousemove', startResizing, false);
   	window.addEventListener('mouseup', stopResizing, false);
}

function startResizing(e) {
   var chatbody = document.getElementById('chat-body');
   var chatdiv = document.getElementById('chat')
   var offset = chatdiv.offsetHeight - chatbody.offsetHeight - (document.getElementById('handle').offsetHeight / 2)
   chatdiv.style.width = noLessThen((window.innerWidth - (e.clientX )) , 370) + 'px';
   chatbody.style.height = ( window.innerHeight   - (e.clientY + offset) ) + 'px';
   console.log(offHg)
   console.log(e.clientY)
}
function stopResizing(e) {
    window.removeEventListener('mousemove', startResizing, false);
    window.removeEventListener('mouseup', stopResizing, false);
}

function noLessThen(x , y){
    return (x < y ? y : x)
}