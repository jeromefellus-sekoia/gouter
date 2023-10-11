import { onMounted } from "vue"
import "./styles/index.scss"
import { UI } from "./App"
import {initWebsocket, websocket_handler} from "./ws"
import {get_stroke, compute_path} from "./utils"

export const Index = {
    setup(props) {
        let drawing = false;

        async function refresh() {
            UI.me = await fetch('/api/me').then(x=>x.json())
            UI.users = await fetch('/api/users').then(x=>x.json())
            UI.draw = await fetch("/api/draw").then(x=>x.json())
            UI.positions = await fetch("/api/positions").then(x=>x.json())
        }

        async function logout() {
            await fetch("/api/logout", { method: "POST" })
            location.replace("/")
        }


        async function onMousemove(e) {
            if(!drawing) {
                await fetch(`/api/move/${e.clientX}/${e.clientY}`,{method:"POST"})
            } else {
                await fetch(`/api/draw/${e.clientX}/${e.clientY}`,{method:"POST"})
            }
        }

        async function onMousedown(e) {
            if(e.button===0) {
                await fetch(`/api/draw/start/${e.clientX}/${e.clientY}`,{method:"POST"})
                drawing = true
            }
        }

        async function onMouseup(e) {
            if(e.button===0) {
                await fetch(`/api/draw/stop`)
                drawing = false
            }
        }

        websocket_handler("move", ({email,x,y})=>{
            UI.positions[email] = [x, y]
        })

        websocket_handler("draw", ({email, x, y})=>{
            UI.positions[email] = [x, y]
            UI.draw[email][UI.draw[email]?.length-1].push([x, y])
        })

        websocket_handler("start_path", ({email, x,y})=>{
            UI.draw[email] ||= []
            UI.draw[email].push([x, y])
        })


        onMounted(initWebsocket)

        refresh()

        return () => {
            return <main onMousemove={onMousemove} onMousedown={onMousedown} onMouseup={onMouseup}>

                <div id="logout">
                    {UI.me} &nbsp;
                    <a href="#" onClick={logout}>logout</a>
                </div>

                <div id="users">
                    {Object.entries(UI.positions||{}).map(([name, pos])=><div style={`color:${get_stroke(name)}`}>{name} ({pos?.[0]},{pos?.[1]})</div>)}
                </div>

                <svg>
                    {Object.entries(UI.draw||{}).map(([name, paths])=><g>
                        {paths?.map(p=><path stroke={get_stroke(name)} stroke-width="3" fill="none" d={compute_path(p)}></path>)}
                    </g>)}
                    {Object.entries(UI.positions||{}).map(([name, [x,y]])=><g transform={`translate(${x},${y})`}><circle r="10"/><text>{name}</text></g>)}
                </svg>


                </main>
        }
    }
}
