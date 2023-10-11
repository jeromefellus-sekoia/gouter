import "./styles/common.scss"
import "./styles/index.scss"
import { reactive } from "vue"
import { useRouter } from "vue-router"
import { ContextMenu } from "./Dropdown"

export const UI = reactive({})


export const App = {
    setup(props) {

        window.addEventListener("click", () => {
            UI.contextMenu = null
        })
        window.addEventListener("keydown", e => {
            if (e.key === "Escape") UI.contextMenu = null
        })

        return () => {
            if (!document.cookie.includes("session=") && !useRouter().currentRoute?.value.path?.includes("login")) useRouter().replace("/login")
            return <>
                <router-view />
                <ContextMenu />
            </>
        }
    }
}