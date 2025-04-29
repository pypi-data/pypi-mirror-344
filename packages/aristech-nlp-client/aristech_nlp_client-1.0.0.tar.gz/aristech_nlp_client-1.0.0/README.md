# Aristech NLP-Client for Python

This is the Python client implementation for the Aristech NLP-Server.

## Installation

The package is not published to PyPI yet but will be soon.

<!-- ```bash
pip install aristech-nlp-client
``` -->

## Usage

```python
from aristech_nlp_client import NlpClient

client = NlpClient(host='nlp.example.com')
data = client.synthesize(SpeechRequest(
    text='Hello, world!',
    options=SpeechRequestOption(
      voice_id='some-voice-id'
    )
))
with open('output.wav', 'wb') as f:
    f.write(data)
```

There are several examples in the [examples](.) directory:

- [functions.py](https://github.com/aristech-de/nlp-clients/blob/main/python/examples/models.py): Demonstrates how to list the available functions.
- [process.py](https://github.com/aristech-de/nlp-clients/blob/main/python/examples/process.py): Demonstrates how to perform NLP processing on a text.
- [projects.py](https://github.com/aristech-de/nlp-clients/blob/main/python/examples/projects.py): Demonstrates how to list the available projects.
- [intents.py](https://github.com/aristech-de/nlp-clients/blob/main/python/examples/intents.py): Demonstrates how to list intents for a project.
- [scoreLimits.py](https://github.com/aristech-de/nlp-clients/blob/main/python/examples/scoreLimits.py): Demonstrates how to use score limits to figure out good thresholds for intents.
- [content.py](https://github.com/aristech-de/nlp-clients/blob/main/python/examples/content.py): Demonstrates how to search content for a given prompt.

You can run the examples directly using `python` like this:

1. Create a `.env` file in the [python](.) directory:

```sh
HOST=nlp.example.com
# The credentials are optional but probably required for most servers:
TOKEN=your-token
SECRET=your-secret

# The following are optional:
# ROOT_CERT=your-root-cert.pem # If the server uses a self-signed certificate
# PROJECT_ID=some-project-id # Required for some examples
```

2. Run the examples, e.g.:

```sh
python examples/functions.py
```
