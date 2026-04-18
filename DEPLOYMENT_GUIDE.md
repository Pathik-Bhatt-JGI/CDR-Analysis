# CDR Forensics Pro - Deployment Guide

## Quick Start (Local)

### Option 1: Run Locally (Easiest)
```bash
pip install -r requirements.txt
streamlit run cdr_forensics_v6_fixed.py
```

The app will open at `http://localhost:8501`

---

## Cloud Deployment Options

### Option 1: Streamlit Cloud (FREE & EASIEST)

1. **Push code to GitHub**
   - Create a GitHub repo
   - Push `cdr_forensics_v6_fixed.py` and `requirements.txt`

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repo, branch, and file
   - Click Deploy

**Pros:** Free, automatic updates, easy
**Cons:** Limited to Streamlit Cloud features

---

### Option 2: Heroku (Paid)

1. **Create Procfile**
```
web: streamlit run cdr_forensics_v6_fixed.py --logger.level=error
```

2. **Create .streamlit/config.toml**
```toml
[server]
port = $PORT
headless = true
runOnSave = true

[client]
showErrorDetails = false
```

3. **Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**Pros:** More control, custom domain
**Cons:** Paid service (~$7/month)

---

### Option 3: AWS (Scalable)

1. **Using EC2**
   - Launch Ubuntu instance
   - Install Python 3.9+
   - Clone repo
   - Run: `streamlit run cdr_forensics_v6_fixed.py`
   - Use Nginx as reverse proxy

2. **Using Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY cdr_forensics_v6_fixed.py .
CMD ["streamlit", "run", "cdr_forensics_v6_fixed.py"]
```

**Pros:** Highly scalable, full control
**Cons:** More complex setup, costs vary

---

### Option 4: Docker + Any Server

1. **Create Dockerfile** (already provided above)

2. **Build & Run**
```bash
docker build -t cdr-forensics .
docker run -p 8501:8501 cdr-forensics
```

3. **Deploy to any server** (DigitalOcean, Linode, etc.)

---

## Recommended: Streamlit Cloud (Easiest)

### Step-by-Step:

1. **Create GitHub Account** (if you don't have one)
   - Go to https://github.com
   - Sign up

2. **Create New Repository**
   - Click "New"
   - Name: `cdr-forensics`
   - Make it Public
   - Click "Create repository"

3. **Upload Files**
   - Click "Add file" → "Upload files"
   - Upload:
     - `cdr_forensics_v6_fixed.py`
     - `requirements.txt`
   - Commit changes

4. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repo
   - Select branch: `main`
   - Select file: `cdr_forensics_v6_fixed.py`
   - Click "Deploy"

5. **Wait 2-3 minutes**
   - Your app will be live at: `https://your-username-cdr-forensics.streamlit.app`

---

## Environment Variables (If Needed)

Create `.streamlit/secrets.toml` for sensitive data:

```toml
[database]
host = "your-db-host"
user = "your-user"
password = "your-password"
```

Access in code:
```python
db_host = st.secrets["database"]["host"]
```

---

## Performance Tips

1. **Cache expensive operations**
```python
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")
```

2. **Use session state for user data**
```python
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
```

3. **Optimize large datasets**
   - Use `@st.cache_data` for data loading
   - Filter data before visualization
   - Use `st.dataframe` with pagination

---

## Monitoring & Logs

### Streamlit Cloud
- Logs visible in deployment settings
- Real-time monitoring dashboard

### Self-Hosted
```bash
# View logs
tail -f streamlit.log

# Monitor resources
top
```

---

## Troubleshooting

### App won't start
```bash
pip install -r requirements.txt --upgrade
streamlit run cdr_forensics_v6_fixed.py --logger.level=debug
```

### Port already in use
```bash
streamlit run cdr_forensics_v6_fixed.py --server.port 8502
```

### Memory issues
- Reduce data size
- Use pagination
- Cache aggressively

---

## Support

For issues:
1. Check Streamlit docs: https://docs.streamlit.io
2. Check GitHub Issues
3. Run diagnostic: `python DIAGNOSE.py`

---

**Recommended:** Use Streamlit Cloud for easiest deployment!
