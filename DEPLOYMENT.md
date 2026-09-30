# Deploying Todo App to Vercel

This guide will help you deploy your Todo App (Frontend + Backend) to Vercel.

## Prerequisites

1. Install [Vercel CLI](https://vercel.com/docs/cli):
   ```bash
   npm i -g vercel
   ```

2. Create a Vercel account at [vercel.com](https://vercel.com)

3. Make sure your project is in a Git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

## Deployment Steps

### Method 1: Using Vercel CLI (Recommended)

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Deploy from the project root:**
   ```bash
   cd c:\Users\HP\OneDrive\Documents\TODOLISTAPP
   vercel
   ```

3. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? (choose your account)
   - Link to existing project? `N`
   - What's your project's name? `todo-app` (or any name you prefer)
   - In which directory is your code located? `./`

4. **Configure build settings:**
   - Vercel will detect it's a monorepo
   - For the frontend: Build command should be `cd frontend && npm run build`
   - Output directory: `frontend/dist`

### Method 2: Using Vercel Dashboard

1. **Push to GitHub:**
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/yourusername/todo-app.git
   git push -u origin main
   ```

2. **Import on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure build settings:
     - Framework Preset: `Vite`
     - Root Directory: `frontend`
     - Build Command: `npm run build`
     - Output Directory: `dist`

## Environment Variables

After deployment, add these environment variables in your Vercel dashboard:

- `VITE_API_URL`: Set to your deployed API URL (e.g., `https://your-app.vercel.app/api/todos`)

## Database Note

⚠️ **Important**: SQLite files are not persistent on Vercel. For production, consider:

1. **Vercel Postgres** (recommended):
   - Add Vercel Postgres integration
   - Update `database.py` to use PostgreSQL

2. **External Database**:
   - Use PlanetScale, Supabase, or Railway
   - Update connection string in environment variables

## Project Structure for Vercel

```
TODOLISTAPP/
├── vercel.json          # Vercel configuration
├── frontend/            # React app
│   ├── package.json
│   ├── dist/           # Build output
│   └── src/
└── backend/            # FastAPI app
    ├── main.py         # API routes
    ├── requirements.txt
    └── database.py
```

## After Deployment

1. Your app will be available at: `https://your-app-name.vercel.app`
2. The API will be available at: `https://your-app-name.vercel.app/api/`
3. Test both the todo functionality and notes feature

## Troubleshooting

- **Build fails**: Check that all dependencies are in `package.json`
- **API not working**: Verify `vercel.json` routes configuration
- **Database issues**: Check if SQLite file permissions are correct
- **CORS errors**: FastAPI CORS middleware should handle this

## Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed