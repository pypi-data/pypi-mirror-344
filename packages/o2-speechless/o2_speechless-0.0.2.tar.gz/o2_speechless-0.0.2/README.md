# speechless

## UV Installation Instructions

To install dependencies and manage the project, we use `uv`, a fast Python package manager and resolver. Follow the steps below to set up your environment.

### Step 1: Install `uv`

You can install `uv` via pip:

```bash
pip install uv
```

Or with `pipx`:

```bash
pipx install uv
```

Verify the installation:

```bash
uv --version
```

### Step 2: Create a Virtual Environment (Optional but Recommended)

You can let `uv` manage the environment for you:

```bash
uv venv
source .venv/bin/activate
```

If you're using your own virtual environment tool (like `venv` or `virtualenv`), just activate it before proceeding.

### Step 3: Install Dependencies

`uv` installs packages directly from `pyproject.toml`. To install all main and development dependencies:

```bash
uv pip compile pyproject.toml --output-file uv.lock
uv pip install --requirements uv.lock
```

### Step 4: Run the Project or Tests

To activate the environment:

```bash
source .venv/bin/activate
```

To run the tests:

```bash
pytest
```

### Step 5: Run pre-commit
To run pre-commit hooks, use:

```bash
uv run pre-commit run --all-files
```

### Step 6: Convert the model to ONNX format

To convert the model to ONNX format, run:

```bash
python export_to_onnx.py --checkpoint /path/to/checkpoint --onnx_model /path/to/onnx_model
```

### Step 7: Add `OPENAI_API_KEY` and/or Set Up `WHISPER_CPP_MODEL`

The `whisper_1` model requires an OpenAI subscription. As an alternative, you can use `whisper.cpp`.

To download a supported model:

```bash
# Linux
docker run -it --rm -v ./data/models:/models ghcr.io/ggerganov/whisper.cpp:main "./models/download-ggml-model.sh small /models"

# Windows (PowerShell)
docker run -it --rm -v "$(pwd -W)/models":/models ghcr.io/ggerganov/whisper.cpp:main "./models/download-ggml-model.sh small /models"
```

Once `WHISPER_CPP_MODEL` is set, inference is handled locally:

```bash
ffmpeg -i data/temp_results/uploaded_audio.mp3 -ar 16000 -ac 1 -c:a pcm_s16le data/audio/output.wav
```

Run whisper.cpp:

```bash
# Linux
docker run -it --rm -v ./data/models:/models -v ./data/audio:/audios ghcr.io/ggerganov/whisper.cpp:main "./build/bin/whisper-cli -m /models/ggml-small.bin -f /audios/output.wav -ml 16 -oj -l en"

# Windows
docker run -it --rm -v "$(pwd -W)/data/models":/models -v "$(pwd -W)/data":/audios ghcr.io/ggerganov/whisper.cpp:main "./build/bin/whisper-cli -m /models/ggml-small.bin -f /audios/output.wav -ml 16 -oj -l en"
```
