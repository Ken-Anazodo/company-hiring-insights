<p>Instructions to Start the Python Web App from a GitHub Repo
📌 Prerequisites
Before you start, ensure you have the following installed:</p>

<p>Python 3.x (Check with python --version or python3 --version)
FastAPI & Uvicorn (Will be installed in steps below)</p>

STEPS:
<p>1.CLONE THE REPOSITORY:
  git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
  cd YOUR_REPO

<p>2.Create a Virtual Environment
  On Linux/macOS: </p>
  <p>python3 -m venv venv
  source venv/bin/activate </p>

  <p>On Windows (CMD):
  python -m venv venv
  venv\Scripts\activate</p>

<p>3. Install Required Dependencies:
   pip install -r requirements.txt</p>

<p>4.Run the FastAPI Server:
  uvicorn pkg:app --host 0.0.0.0 --port 8000 --reload</p>
   

