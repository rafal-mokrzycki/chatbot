# ChatBot


## Getting started

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate your virtual environment:

```bash
venv/Scripts/Activate.ps1
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Create a Pinecone index and/or manupalate data in it:

```bash
python run.py [-h] [--create_index] [--recreate_index]  [--delete_index] [--delete_data] [--load_data]

create_index - flag to create a new index with a default name taken from config.json
recreate_index - flag to recreate a new index with a default name taken from config.json
delete_index - deletes an index with a given name
delete_data - deletes all data in a given namespace. Default to be found in config.json
load_data - loads data from a CSV file to an index
```

5. Run ChatBot:

```bash
python main.py
```
