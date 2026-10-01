# ComicCraft

ComicCraft is an AI-powered five-panel comic generator.

## Features

- FastAPI backend
- Jinja2 frontend
- Gemini story generation
- Five-panel comic outline
- Narration and dialogue generation
- Stable Diffusion image generation
- Hugging Face image generation
- Local image generation
- PDF export
- REST API
- Swagger documentation
- Demo mode
- Automated tests

---

# Installation

## 1. Open the project

Open the ComicCraft directory in VS Code.

---

## 2. Create a virtual environment

Windows:

```powershell
py -3.11 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 3. Run the application

From the project root:

```powershell
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.