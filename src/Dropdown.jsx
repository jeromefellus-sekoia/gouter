import { UI } from "./App";
import "./styles/dropdown.scss"

export const Dropdown = {
    setup(props, { slots }) {
        return () => {
            return <div class='_dropdown'>
                {slots?.default?.()}
            </div>
        }
    }
}

function updateContextMenuPosition() {
    UI.contextMenuY = UI.contextMenuAnchor.getBoundingClientRect().top + UI.contextMenuAnchor.offsetHeight
    UI.contextMenuX = UI.contextMenuAnchor.getBoundingClientRect().left
}


function removeEventListenerAncestors(e, evt, listener) {
    while (e) {
        e.removeEventListener(evt, listener)
        e = e.parentElement
    }
}

function addEventListenerAncestor(e, evt, listener) {
    while (e) {
        e.addEventListener(evt, listener)
        e = e.parentElement
    }
}

export function contextMenu(anchor, e) {

    if (UI.contextMenuAnchor) removeEventListenerAncestors(UI.contextMenuAnchor, "scroll", updateContextMenuPosition)

    UI.contextMenuY = anchor.getBoundingClientRect().top + anchor.offsetHeight
    UI.contextMenuX = anchor.getBoundingClientRect().left
    UI.contextMenuAnchor = anchor
    UI.contextMenu = e


    addEventListenerAncestor(UI.contextMenuAnchor, "scroll", updateContextMenuPosition)
}

export const ContextMenu = {
    setup(props) {
        return () => {
            return UI.contextMenu && <div id="context-menu" style={{ left: UI.contextMenuX + "px", top: UI.contextMenuY + "px" }}>
                {UI.contextMenu}
            </div>
        }
    }
}