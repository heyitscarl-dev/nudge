# nudge
An email-wrapped AI agent written in python.

## introduction

Nudge is an AI-agent at its code. However, instead of any fancy website, I chose to use email
as the only form of UI.

## tooling

| Tool          | Purpose                                       |
| ------------- | --------------------------------------------- |
| Mailgun       | Receive & Send Emails                         |
| OpenAI        | Generate responses                            |

## self-hosting

### prerequisites

- [ `asdf-vm` ](https://asdf-vm.com)
- [ `python` ](https://www.python.org)
- a domain name & the ability to host local services on that domain (i.e. cloudflare tunnels)
- a mailgun account (set up for sending & receiving emails on your domain), api key and webhook signing key
- an openai account and api key

### installation 

1. Clone this repository

```bash
git clone https://github.com/heyitscarl-dev/nudge.git
cd nudge
```

2. Create a virtual environment using `venv`

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies using `pip`

```bash
pip install -r requirements.txt
```

4. Add your credentials to a `.env` file

- `MAILGUN_API_KEY`
- `MAILGUN_DOMAIN` (include subdomain)
- `MAILGUN_WEBHOOK_SIGNING_KEY`
- `OPENAI_API_KEY`

5. Start `fastapi`

```bash 
fastapi run main.py
```

## usage

Now that you're hosting Nudge, simply send your first mail to the email address you configured in mailgun, e.g. `nudge@yourdomain.com`
