from flask import Blueprint, request, render_template
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')



#------SETTING UP ROUTES------



#route to show index page

@webhook.route('/', methods=["GET"])
def index():
    # This will look for index.html in app/templates/
    return render_template('index.html')



#---schema to store events---
def save_event(data_type, author, from_b, to_b, req_id, msg):
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
    mongo.db.events.insert_one({
        "request_id": req_id,
        "author": author,
        "action": data_type,
        "from_branch": from_b,
        "to_branch": to_b,
        "timestamp": timestamp,
        "display_message": msg
    })


#--- webhook route to receive github events ---    

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    print(data)  # For debugging purposes
    event = request.headers.get('X-GitHub-Event')
    author = data.get('sender', {}).get("login")
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')

    if event == "push":
        branch = data.get("ref").split("/")[-1]
        req_id = data.get('after')
        msg = f'"{author}" pushed to "{branch}" on {timestamp}'
        save_event("PUSH", author, branch, branch, req_id, msg)

    elif event == "pull_request":
        pr = data.get("pull_request")
        from_b = pr.get("head", {}).get("ref")
        to_b = pr.get("base", {}).get("ref")
        req_id = str(pr.get("id"))
        
        if data.get("action") == "closed" and pr.get("merged"):
            msg = f'"{author}" merged branch "{from_b}" to "{to_b}" on {timestamp}'
            save_event("MERGE", author, from_b, to_b, req_id, msg)
        elif data.get("action") == "opened":
            msg = f'"{author}" submitted a pull request from "{from_b}" to "{to_b}" on {timestamp}'
            save_event("PULL_REQUEST", author, from_b, to_b, req_id, msg)

    return {}, 200

#---api to fetch last events---
@webhook.route('/data', methods=["GET"])
def get_data():
    events = list(mongo.db.events.find({}, {'_id': 0}).sort('_id', -1).limit(10))
    return {"events": events}, 200