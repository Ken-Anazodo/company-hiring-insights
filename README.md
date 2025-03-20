
    <div class="section">
        <h2>📌 Prerequisites</h2>
        <p>Before you start, ensure you have the following installed:</p>
        <ul>
            <li>Python 3.x (Check with <code>python --version</code> or <code>python3 --version</code>)</li>
            <li>FastAPI & Uvicorn (Will be installed in steps below)</li>
        </ul>
    </div>

    <div class="section">
        <h2>✅ Steps to Set Up</h2>
        
        <h3>1️⃣ Clone the Repository</h3>
        <pre><code>git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO</code></pre>

        <h3>2️⃣ Create a Virtual Environment</h3>
        <p><strong>On Linux/macOS:</strong></p>
        <pre><code>python3 -m venv venv
source venv/bin/activate</code></pre>
        <p><strong>On Windows (CMD):</strong></p>
        <pre><code>python -m venv venv
venv\Scripts\activate</code></pre>

        <h3>3️⃣ Install Required Dependencies</h3>
        <pre><code>pip install -r requirements.txt</code></pre>

        <h3>4️⃣ Run the FastAPI Server</h3>
        <pre><code>uvicorn pkg:app --host 0.0.0.0 --port 8000 --reload</code></pre>
    </div>

    <div class="section">
        <h2>🚀 Additional Features to Implement (If More Time Available)</h2>
        <ul>
            <li><strong>📉 Salary Range Analysis</strong>
                <ul>
                    <li>Calculate average salary per industry.</li>
                    <li>Identify companies offering the highest salaries.</li>
                </ul>
            </li>
            <li><strong>📊 Job Growth Trends Over Time</strong>
                <ul>
                    <li>If job postings include a timestamp, track how hiring changes over time.</li>
                    <li>Use line charts to visualize trends.</li>
                </ul>
            </li>
            <li><strong>📍 State & City Comparisons</strong>
                <ul>
                    <li>Show which states/cities have the highest job growth.</li>
                    <li>Add filters for users to explore trends.</li>
                </ul>
            </li>
            <li><strong>🔎 Search Bar for Companies</strong>
                <ul>
                    <li>Instead of a dropdown, implement a searchable input field.</li>
                    <li>Suggest autocompleted company names.</li>
                </ul>
            </li>
            <li><strong>🔄 Filtering & Sorting on UI</strong>
                <ul>
                    <li>Allow users to filter by industry, job role, or city.</li>
                    <li>Add sorting options (highest-paying jobs, most openings, etc.).</li>
                </ul>
            </li>
            <li><strong>🌍 Map Visualization for Job Openings</strong>
                <ul>
                    <li>Use Leaflet.js or Google Maps API to display job postings geographically.</li>
                    <li>Color-code based on job demand per city/state.</li>
                </ul>
            </li>
        </ul>
    </div>
</body>
</html>
