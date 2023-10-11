import asyncio
from fastapi import FastAPI, Body, Depends, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.draw import PATHS, POSITION
from api.ws import USERS, WEBSOCKETS, notify_all, on_ws_receive
from api.auth import (
    authenticated,
    Session,
    parse_session_cookie,
    session,
    login_from_google,
)
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
    try:
        jwt = login_from_google(credential)[0]
        r = JSONResponse({})
        r.set_cookie("session", jwt)
        return r
    except Exception as e:
        print(e)
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


@app.get("/api/users")
@authenticated
def get_users(s: Session = Depends(session)):
    return list(USERS)


@app.get("/api/draw")
@authenticated
def _get_draw(s: Session = Depends(session)):
    return PATHS


@app.get("/api/positions")
@authenticated
def _get_positions(s: Session = Depends(session)):
    return POSITION


@app.post("/api/move/{x}/{y}")
@authenticated
def _move(x: float, y: float, s: Session = Depends(session)):
    POSITION[s.email] = (x, y)
    asyncio.run(notify_all({"msg": "move", "x": x, "y": y, "email": s.email}))
    return True


@app.post("/api/draw/{x}/{y}")
@authenticated
def _draw(x: float, y: float, s: Session = Depends(session)):
    POSITION[s.email] = (x, y)
    PATHS[s.email][-1].append((x, y))
    asyncio.run(notify_all({"msg": "draw", "x": x, "y": y, "email": s.email}))
    return True


@app.post("/api/draw/start/{x}/{y}")
@authenticated
def _start_path(x: float, y: float, s: Session = Depends(session)):
    PATHS[s.email].append([(x, y)])
    asyncio.run(notify_all({"msg": "start_path", "x": x, "y": y, "email": s.email}))
    return True


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        user = parse_session_cookie(websocket.cookies["session"])
        if not user:
            raise HTTPException(401)
        print(user.email, "connected")
        WEBSOCKETS.append(websocket)
        if user:
            USERS.add(user.email)
        print(len(WEBSOCKETS), "clients connected now")
        while True:
            on_ws_receive(websocket, await websocket.receive())
    except Exception:
        if user:
            print(user.email, "disconnected")
            try:
                USERS.remove(user.email)
            except Exception:
                ...
        try:
            WEBSOCKETS.remove(websocket)
        except Exception:
            ...
        print(len(WEBSOCKETS), "clients connected now")


# Serve single page vue3 application
if isdir("./dist"):
    app.mount(path="/", app=SinglePageApplication(directory="./dist"), name="spa")
