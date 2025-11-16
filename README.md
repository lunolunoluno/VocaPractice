# VocaPractice

## Requirements

- **Python version >3.10**
- [A Google Gemini API Key](https://aistudio.google.com/app/api-keys)

### Setup

It is recommended to create a Python [virtual environment](https://docs.python.org/3/library/venv.html)
```sh
python3 -m venv .venv
source .venv/bin/activate       # macOS / Linux
# or
.\.venv\Scripts\activate        # Windows
```

Then install dependencies:

```sh
pip install -r requirements.txt
```

# Run

Start the application with:

```sh
python main.py
```

After launching, Gradio will print a local URL in the terminal (typically http://127.0.0.1:7860).
Open this link in your browser to access the app.
