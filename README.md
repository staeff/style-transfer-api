# Style transfer web app

Based on [https://github.com/amalshaji/style-transfer](https://github.com/amalshaji/style-transfer)

## Setup

* Install Python dependencies for frontend and backend

```sh
$ make install
```

* Download the machine learning models

```sh
$ make backend/models
```

* Build the `frontend` and `backend` container and run them

```sh
$ docker-compose up -d --build
```

* Visit [http://localhost:8501](http://localhost:8501) and upload an image


## Features

* a `backend` that is an asynchronous API (FastAPI) to serve a machine learning model

* a `frontend` UI with Streamlit

* `backend` and `frontend` are containerized with Docker

* `asyncio` code executed in the background outside the request/response flow

## Style transfer and models

Style transfer is an image transformation operation, where an input image is transformed into an output image.
Its goals is to pick up the style of an image which is represented in a trained model and apply to another image.
The 2016 [Perceptual Losses for Real-Time Style Transfer and Super-Resolution](https://cs.stanford.edu/people/jcjohns/eccv16/) paper introduced `fast-style transfer`,
which allows to style any image in a single pass, instead of multiple runs.

The research described in the article created nine different trained models, which will be used in this demo.
