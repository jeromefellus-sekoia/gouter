import { onMounted, reactive } from "vue"
import "./styles/index.scss"
import { UI } from "./App"

export const Index = {
    setup(props) {
        let ws = null;
        const data = reactive({})

        async function refresh() {
            UI.me = await fetch('/api/me').then(x=>x.json())
        }

        async function logout() {
            await fetch("/api/logout", { method: "POST" })
            location.replace("/")
        }

        async function onWebsocketMessage(msg) {
            console.log(msg)
        }


        async function initWebsocket() {
            if(ws) ws.close()
            ws = new WebSocket(`${location.protocol==="http:" ? "ws" : "wss"}://${location.hostname}:8001/ws`)
            // ws.onopen = ()=>{
            //     ws.send("youpi")
            // }
            // ws.onmessage = onWebsocketMessage
            // ws.onerror = ()=>setTimeout(initWebsocket, 1000)
            // ws.onclose = ()=>setTimeout(initWebsocket, 1000)
        }

        onMounted(initWebsocket)

        refresh()

        return () => {
            return <main>

                <div id="logout">
                    <a href="#" onClick={logout}>logout</a>
                </div>


                </main>
        }
    }
}