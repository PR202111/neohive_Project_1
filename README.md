# Resume Builder Project

**Google Drive Direct Link:**  
[Watch Demo Video](https://drive.google.com/file/d/1LvdMo2mcQ1Zx-SLtdCQHn-gwsbgC5P-B/view?usp=sharing)

This project is a Resume Builder application that allows users to generate and review professional resumes.

Key Files:

* builder.py – Handles resume creation logic
* reviewer.py – Handles resume review and suggestions
* main.py – FastAPI backend API
* ui.py – Streamlit frontend UI
* run.py – Starts both backend and frontend
* requirements.txt – Project dependencies

Built with Python 3.13.

Setup Instructions:

1. Clone the repository:

```
git clone https://github.com/your-username/resume-builder.git
cd resume-builder
```

2. Create and activate a virtual environment:

```
python3.13 -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. Install dependencies:

```
pip install --upgrade pip
pip install -r requirements.txt
```

4. Run the application:

```
python run.py
```

* Streamlit UI will open at [http://localhost:8501](http://localhost:8501)
* FastAPI backend will run at [http://localhost:8000](http://localhost:8000)

File Structure:

```
.
├── builder.py
├── reviewer.py
├── main.py
├── ui.py
├── run.py
├── requirements.txt
└── README.md
```

Demo Video:
Replace the link below with your Google Drive or YouTube link:

```
[![Watch the demo](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID/0.jpg)](https://your-video-link.com)
```

Notes:

* Ensure you are using Python 3.13
* Large video files should be hosted externally and linked in the README
* Use a virtual environment to avoid dependency conflicts
