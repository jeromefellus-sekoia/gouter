from fastapi import FastAPI, Body, Depends, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.draw import PATHS, POSITION
from api.ws import WEBSOCKETS, notify_all, on_ws_receive
from api.auth import authenticated, Session, session, login_from_google
from api.spa import SinglePageApplication
from os.path import isdir

ENV = "prod"

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/login")
def login(credential: str = Body(embed=True)):
    print(credential)
    try:
        jwt = login_from_google(credential)
        r = JSONResponse({})
        r.set_cookie("session", jwt)
        return r
    except Exception as e:
        raise HTTPException(401)


@app.post("/api/logout")
def logout():
    r = JSONResponse("ok")
    r.delete_cookie("session")
    return r


@app.get("/api/me")
@authenticated
def get_me(s: Session = Depends(session)):
    return s.email


@app.get("/api/me")
@authenticated
def get_me(s: Session = Depends(session)):
    return s.email


@app.post("/api/move/{x}/{y}")
@authenticated
async def _move(x: float, y: float, s: Session = Depends(session)):
    POSITION[s.email] = (x, y)
    await notify_all({"msg": "move", "x": x, "y": y, "email": s.email})


@app.post("/api/draw/{x}/{y}")
@authenticated
async def _draw(x: float, y: float, s: Session = Depends(session)):
    PATHS[s.email][-1].append((x, y))
    await notify_all({"msg": "draw", "x": x, "y": y, "email": s.email})


@app.post("/api/path/start/{x}/{y}")
@authenticated
async def _start_path(x: float, y: float, s: Session = Depends(session)):
    PATHS[s.email].append([])
    PATHS[s.email][-1].append((x, y))
    await notify_all({"msg": "start_path", "x": x, "y": y, "email": s.email})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        WEBSOCKETS.append(websocket)
        print(len(WEBSOCKETS), "clients connected now")
        while True:
            on_ws_receive(websocket, await websocket.receive())
    except Exception:
        WEBSOCKETS.remove(websocket)
        print(len(WEBSOCKETS), "clients connected now")


# Serve single page vue3 application
if isdir("./dist"):
    app.mount(path="/", app=SinglePageApplication(directory="./dist"), name="spa")
