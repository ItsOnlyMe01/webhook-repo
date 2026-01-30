TechStax Assignment--

webhook receiver--

This is my implementation for the Flask webhook receiver task. i have set up the project structure using blueprints and connected it to mongodb.

What I added:

    1.The app now connects to a local Mongo instance to save the webhook data.

    2.I added a simple UI to see the last 10 events without having to check the database manually.

    3.The routes are organized under the "/webhook" prefix.

How to run it:

    setup the environment
    Bash

    python -m venv venv
    .\venv\Scripts\activate

    install libraries
    Bash

    pip install -r requirements.txt

    start the server
    Bash

    python run.py

Where to test:

    Receiver: POST http://127.0.0.1:5000/webhook/receiver.

    UI: http://127.0.0.1:5000/webhook/
