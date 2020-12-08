from starlette.applications import Starlette
import uvicorn
import os

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from camera import Camera
from image_processor import ImageProcessor

templates = Jinja2Templates(directory='templates')

app = Starlette()
app.mount('/static', StaticFiles(directory='static'), name='static')

camera = Camera(ImageProcessor())

@app.route("/", methods=["GET"])
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket_route('/ws')
async def websocket_endpoint(websocket):
    await websocket.accept()
    while True:
        mesg = await websocket.receive_text()
        parts = mesg.split(",")
        camera.enqueue_input(parts[1])
        processed = camera.get_frame()
        parts[1] = processed
        output = ",".join(parts)
        await websocket.send_text(output)
    await websocket.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8008))
    uvicorn.run(app, host="0.0.0.0", port=port)
    # app.run()
