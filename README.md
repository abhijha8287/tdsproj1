# LLM Automation Agent (TDS Project 1)

A FastAPI service that takes a plain-English task, works out which operation it means and runs it on local files.

## Why this exists
Project 1 of the Tools in Data Science (TDS) course in the IIT Madras BS in Data Science, January 2025 term.

## What it does
- `POST /run?task=...`: uses an LLM to map the task to a function, then runs it
- `GET /read?path=...`: returns the contents of a file
- Phase A tasks (`tasksA.py`): generate data, format Markdown with Prettier, count weekdays in dates, sort contacts, collect recent logs, index docs, extract an email sender, read a card number from an image, find similar comments with embeddings, query a SQLite database
- Phase B tasks (`tasksB.py`): fetch from APIs, run SQL, scrape websites, resize images, convert Markdown to HTML

## Project structure
```
tdsproj1/
├── app.py            FastAPI app and task routing
├── tasksA.py         Phase A task functions
├── tasksB.py         Phase B task functions
├── datagen.py        Creates the test data
├── evaluate.py       Course evaluation script
├── Dockerfile        Image with Python and Node
├── requirements.txt  Python dependencies
└── LICENSE           MIT licence
```

## Getting started
Requirements: Docker, or Python 3.11+ with Node.js 18 (for Prettier).
```bash
git clone https://github.com/abhijha8287/tdsproj1.git
cd tdsproj1
docker build -t tds-agent .
docker run -p 8000:8000 -e AIPROXY_TOKEN=... tds-agent
curl -X POST "http://localhost:8000/run?task=Sort%20/data/contacts.json%20by%20last_name"
```

## Configuration
| Variable | Purpose |
|:--|:--|
| `AIPROXY_TOKEN` | Token for the course's OpenAI proxy |

## Tech stack
Python, FastAPI, OpenAI API (via AI Proxy), SQLite, Docker, Node.js (Prettier)

## Notes
MIT licensed.
