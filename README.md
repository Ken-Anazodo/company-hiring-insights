<p>Instructions to Start the Python Web App from a GitHub Repo</p>
<p>📌 Prerequisites</p>
<p>Before you start, ensure you have the following installed:</p>

<p>Python 3.x (Check with python --version or python3 --version)</p>
<p>FastAPI & Uvicorn (Will be installed in steps below)</p>

STEPS:
<ul>
<li>CLONE THE REPOSITORY:</li>
  <p>git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git</p>
  <p>cd YOUR_REPO</p>

<li>Create a Virtual Environment
  <p>On Linux/macOS: </p>
  <p>python3 -m venv venv</p>
  <p>source venv/bin/activate</p> </li>

  <li>On Windows (CMD):
  <p>python -m venv venv</p>
 <p> venv\Scripts\activate</p></li>

<li>Install Required Dependencies:
  <p></p> pip install -r requirements.txt</p></li>

<li>Run the FastAPI Server:
  <p>uvicorn pkg:app --host 0.0.0.0 --port 8000 --reload</p></li>
</ul>
   

