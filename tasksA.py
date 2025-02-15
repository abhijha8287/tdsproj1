import sqlite3
import subprocess
from dateutil.parser import parse
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
import base64
from fastapi import HTTPException

load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')


def A1(email="23f3004013@ds.study.iitm.ac.in",url="https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"):
    try:
        process = subprocess.Popen(
            ["uv", "run", url, "--root", "./data", email],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {stderr}")
        return stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")


def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    # Correcting the command list syntax by adding a comma
    command = ["npx", "--yes", prettier_version, "--write", filename.lstrip("/")]
    
    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
        return None  # No need to read the file again
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print(f"Error output: {e.output}")
        return None

def A3(filename='/data/dates.txt', targetfile='/data/dates-wednesdays.txt', weekday=2):
    input_file = Path(filename.lstrip("/"))
    output_file = Path(targetfile.lstrip("/"))
    weekday_count = 0

    with input_file.open('r') as file:
        weekday_count = sum(1 for date in file if parse(date).weekday() == int(weekday)-1)

    with output_file.open('w') as file:
        file.write(str(weekday_count))

def A4(filename="/data/contacts.json", targetfile="/data/contacts-sorted.json"):
    input_file = Path(filename.lstrip("/"))
    output_file = Path(targetfile.lstrip("/"))
    
    with input_file.open('r') as file:
        contacts = json.load(file)

    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

    with output_file.open('w') as file:
        json.dump(sorted_contacts, file, indent=4)

def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    log_dir = Path(log_dir_path.lstrip("/"))
    output_file = Path(output_file_path.lstrip("/"))

    log_files = sorted(log_dir.glob('*.log'), key=os.path.getmtime, reverse=True)[:num_files]

    with output_file.open('w') as f_out:
        for log_file in log_files:
            with log_file.open('r') as f_in:
                first_line = f_in.readline().strip()
                f_out.write(f"{first_line}\n")

def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    docs_dir = Path(doc_dir_path.lstrip("/"))
    output_file = Path(output_file_path.lstrip("/"))
    index_data = {}

    # Traverse through all files in docs_dir
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                with file_path.open('r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('# '):  # First H1 title found
                            title = line[2:].strip()  # Remove the '# ' and strip whitespace
                            relative_path = str(file_path.relative_to(docs_dir)).replace('\\', '/')
                            index_data[relative_path] = title
                            break  # Only take the first H1 title

    # Sort the index data by the filenames (keys)
    sorted_index_data = {k: index_data[k] for k in sorted(index_data)}

    # Write the index data to the output file
    with output_file.open('w', encoding='utf-8') as f:
        json.dump(sorted_index_data, f, indent=4)

def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    input_file = Path(filename.lstrip("/"))
    output_file = Path(output_file.lstrip("/"))
    
    with input_file.open('r') as file:
        email_content = file.readlines()

    sender_email = "sujay@gmail.com"
    for line in email_content:
        if "From" == line[:4]:
            sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
            break

    with output_file.open('w') as file:
        file.write(sender_email)

def png_to_base64(image_path):

    with image_path.open("rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string

def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    input_file = Path(filename.lstrip("/"))
    image_path = Path(image_path.lstrip("/"))
    
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the fake credit card number from the image, 4 group of 4 digits like a credit card number, only extract the those digit number without spaces and return just the number without any other characters"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                             headers=headers, data=json.dumps(body))

    result = response.json()
    card_number = result['choices'][0]['message']['content'].replace(" ", "")

    with input_file.open('w') as file:
        file.write(card_number)


def get_embeddings(comments: list):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    payload = {
        "model": "text-embedding-3-small",
        "input": comments  # Accepting a list of strings
    }
    response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return [item['embedding'] for item in data['data']]
    else:
        raise Exception(f"Error fetching embeddings: {response.text}")

def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    input_file = Path(filename.lstrip("/"))
    output_file = Path(output_filename.lstrip("/"))
    
    with input_file.open('r') as f:
        comments = [line.strip() for line in f.readlines()]

    # Get embeddings for all comments in a single request
    embeddings = get_embeddings(comments)

    min_distance = float('inf')
    most_similar = (None, None)

    # Compare all pairs of embeddings
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = cosine(embeddings[i], embeddings[j])
            if distance < min_distance:
                min_distance = distance
                most_similar = (comments[i], comments[j])

    # Write the most similar pair to the output file
    with output_file.open('w') as f:
        f.write(most_similar[0] + '\n')
        f.write(most_similar[1] + '\n')

def A10(filename='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt', query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    db_file = Path(filename.lstrip("/"))
    output_file = Path(output_filename.lstrip("/"))
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(query)
    total_sales = cursor.fetchone()[0]
    total_sales = total_sales if total_sales else 0

    with output_file.open('w') as file:
        file.write(str(total_sales))

    conn.close()