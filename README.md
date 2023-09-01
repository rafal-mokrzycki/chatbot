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
load_data - loads data from a directory ./data into a CSV file and then to an index
```

5. Run ChatBot:

```bash
python main.py
```

## Quick HOWTO

1. How do I create and index?

By populating `config.json` with your access data and then running:

```python run.py --create_index```

2. How do I load data into an index?

First, upload your data into `./data` directory in the root. Make sure the data is clean.
Then make sure you have the right access data in `config.json`. Then run:

```python run.py --load_data```

or

```python loader.py```

3. How do I remove data from an index?

To remove all data from a namespace in the default index run:

```python run.py --delete_data {namespace}```

For now, deleting all data from all namespaces is not supported, you have to delete
all data from your all namespaces separately. Also, deleting some data from a namespace
is not supported yet.

4. What does 'recreate an index' mean.

If you run:

```python run.py --recreate_index```

all data in the index qill be removed, the index qill be deleted and created again. It will epmty, obviuosly, so to populate data in it, see point 2.

5. How can I 'talk' to the chatbot?

I order to talk to the chatbot you run:

```python run.py --make_conversation```

then the chatbot asks you, what you would like to ask it about. You can just type in your question(s) (one at a time) and waitfor response. To quit, hit 'q'. Additionally, you can add flag `--verbose` or `-v` to see the distance between query vector and answer vector.

6. Is there a different way to test the program?

Yes, there are two ways to test it. First is to directly run main.py:

```python scripts/main.py```

There are predefined questions and you can see how the model dealswith them. Another way is to run:

```python func_tests/main.py```

This script generates a `answers.csv` file with two columns: one with queries and the secind one with answers, and you can see, how the model performed or predefined questions that can be found in questies.txt. Alternatively, you can type in your own questions in `questies.txt` and then run the `func_tests/main.py` script.

Of course, there are also unit tests in the `tests` directory. To perform them, run:

```python -m pytest -vv  tests/test_loader.py -s```

or

```python -m pytest -vv  tests/test_parser.py -s```.
