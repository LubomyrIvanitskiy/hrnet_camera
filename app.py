from starlette.applications import Starlette
import uvicorn
import os
import asyncio
import threading

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from camera import Camera
from image_processor import ImageProcessor

templates = Jinja2Templates(directory='templates')

app = Starlette()
app.mount('/static', StaticFiles(directory='static'), name='static')

camera = Camera(ImageProcessor())

sockets = []


@app.route("/", methods=["GET"])
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket_route('/ws')
async def websocket_endpoint(websocket):
    global sockets
    sockets.append(websocket)

    await websocket.accept()
    while True:
        try:
            mesg = await websocket.receive_text()
            camera.enqueue_input(mesg)
        except Exception as e:
            websocket.remove(websocket)

    await websocket.close()


async def answer():
    """Video streaming generator function."""
    while True:
        print("SOCKETS", len(sockets))
        if len(sockets) > 0:
            frame = camera.get_frame()
            for websocket in sockets:
                await websocket.send_text(frame)
        else:
            await asyncio.sleep(2)


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(answer())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    import threading

    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()

    port = int(os.environ.get("PORT", 8008))
    uvicorn.run(app, host="0.0.0.0", port=port)
    app.run()
