# Deploy Backend to Render

## Quick Deploy Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare backend for Render deployment"
   git push
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repo: `ELIZA-22/TODOLISTAPP`

3. **Configure Render:**
   - **Name**: `todo-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. **After Deploy:**
   - Copy your Render URL (e.g., `https://todo-backend-xxx.onrender.com`)
   - Update frontend API URLs to use this URL
   - Redeploy frontend to Vercel

## Backend Files Ready:
✅ `render.yaml` - Render configuration
✅ `requirements.txt` - Updated with uvicorn[standard]
✅ `main.py` - CORS configured for production
✅ `.env.example` - Environment variables template

## API Endpoints:
- Root: `https://your-render-url.com/`
- Todos: `https://your-render-url.com/api/todos`
- Notes: `https://your-render-url.com/api/notes`
- Docs: `https://your-render-url.com/docs`