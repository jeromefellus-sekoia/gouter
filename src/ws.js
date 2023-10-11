let websocket = null

const HANDLERS = {}

export function websocket_handler(msg, handler) {
    HANDLERS[msg] = handler
}


async function onWebsocketMessage(msg) {
    try {
        msg = JSON.parse(msg.data)
        console.log(msg)
        HANDLERS[msg.msg](msg)
    } catch(e){
        console.warn(`Websocket message ${msg} error`)
    }
}


export function initWebsocket(path="websocket") {
    if(websocket) websocket.close()
    websocket = new WebSocket(`${location.protocol==="http:" ? "ws" : "wss"}://${location.host}/${path}`)
    websocket.onmessage = onWebsocketMessage
    // websocket.onerror = ()=>setTimeout(initWebsocket, 1000)
    websocket.onclose = ()=>setTimeout(initWebsocket, 1000)
}
