import os
import flask
import requests
import dotenv

app = flask.Flask(__name__)

def main():
    dotenv.load_dotenv()
    res = send("carl.nw.neben@gmail.com", "Test", "This is a test message, automatically sent by `nudge`.")
    print(res.text)
    app.run(port=5000)

@app.route("/mailgun/incoming", methods=["POST"])
def receive():
    sender = flask.request.form.get("sender")
    subject = flask.request.form.get("subject")
    body_plain = flask.request.form.get("body-plain")

    print(f"Email from {sender}: {subject}")
    print(body_plain)

    return "OK", 200


def send(
    to,
    subject, 
    text, 
    domain=None, 
    api_key=None
):
    return requests.post(
        f"https://api.eu.mailgun.net/v3/{domain or os.getenv("MAILGUN_DOMAIN") or exit(1)}/messages",
        auth=("api", api_key or os.getenv("MAILGUN_API_KEY") or exit(2)),
        data={
            "from": "Nudge <nudge@mg.heyitscarl.dev>",
            "to": to,
            "subject": subject,
            "text": text,
        }
    )

if __name__ == "__main__":
    main()
