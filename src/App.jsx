import "./styles/common.scss"
import "./styles/index.scss"
import { reactive } from "vue"
import { ContextMenu } from "./Dropdown"

export const UI = reactive({
    draw:{},
    positions:{},
})


export const App = {
    setup(props) {

        window.addEventListener("click", () => {
            UI.contextMenu = null
        })
        window.addEventListener("keydown", e => {
            if (e.key === "Escape") UI.contextMenu = null
        })

        return () => {
            if (!document.cookie.includes("session=") && !location.pathname?.endsWith("login")) location.replace("/login")
            return <>
                <router-view />
                <ContextMenu />
            </>
        }
    }
}