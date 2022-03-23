import asyncio
import time
import uuid
from concurrent.futures import ProcessPoolExecutor
from functools import partial

import cv2
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
import numpy as np
from PIL import Image

import config
import inference


app = FastAPI()


@app.get("/")
def read_root():
    """Dummy endpoint to show that the api is serving"""
    return {"message": "Welcome from the API"}


async def combine_images(output, resized, name):
    final_image = np.hstack((output, resized))
    cv2.imwrite(name, final_image)


@app.post("/{style}")
async def get_image(style: str, file: UploadFile = File(...)):
    """
       Endpoint that receives a model name and image file
       and sents it to the inference function

       style: name of the model that should be used
       file: image accepted as a file over a POST request


    """
    image = np.array(Image.open(file.file))
    model = config.STYLES[style]
    start = time.time()
    output, resized = inference.inference(model, image)
    name = f"/storage/{str(uuid.uuid4())}.jpg"
    print(f"name: {name}")
    # name = file.file.filename
    cv2.imwrite(name, output)
    models = config.STYLES.copy()
    del models[style]
    asyncio.create_task(generate_remaining_models(models, image, name))
    return {"name": name, "time": time.time() - start}


async def generate_remaining_models(models, image, name: str):
    """"""
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image, name)
    )


def process_image(models, image, name: str):
    """Process an image with the selected style synchronously"""
    for model in models:
        output, resized = inference.inference(models[model], image)
        name = name.split(".")[0]
        name = f"{name.split('_')[0]}_{models[model]}.jpg"
        cv2.imwrite(name, output)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
