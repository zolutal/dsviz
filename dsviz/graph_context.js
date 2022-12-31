/* Credit: https://stackoverflow.com/questions/60044441/context-menus-for-nodes-and-edges-for-dot-graphs-using-python */

const svg = document.querySelector("#graph > svg")
const rowMenu = document.querySelector("#row_context_menu");

const g = svg.childNodes[1];
let selected;

function addMenu(node, menu) {
    node.addEventListener("contextmenu", e => {
        menu.style.left = `${e.pageX}px`;
        menu.style.top = `${e.pageY}px`;

        selected = node.id;

        setMenuVisible(true, menu);
        e.preventDefault();
        e.stopPropagation();
    });
}

for(let node of g.childNodes) {
    if(node.tagName === "g"){
      for(let n_node of node.childNodes) {
        if(n_node.tagName === "g"){
          addMenu(n_node, rowMenu);
        }
      }
    }
}

function setMenuVisible(visible, menu) {
    if(visible) {
        setMenuVisible(false);
    }
    if(menu) {
        menu.style.display = visible ? "block" : "none";
    } else {
        setMenuVisible(visible, rowMenu);
    }
}

window.addEventListener("click", e => {
    setMenuVisible(false);
});
window.addEventListener("contextmenu", e => {
    setMenuVisible(false);
    e.preventDefault();
});


function menuClick(menuType, item) {
    console.log(menuType + ", " + item + ", "+selected);
    if(menuType === 'edge') {
        selected = selected.replace('&gt;','>');
    }
  pywebview.api.menu_item_clicked(menuType,selected,item);
}
