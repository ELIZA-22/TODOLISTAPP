# PowerShell deployment script for Vercel

Write-Host "🚀 Deploying Todo App to Vercel..." -ForegroundColor Green

# Check if Vercel CLI is installed
if (!(Get-Command "vercel" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
}

# Check if git is initialized
if (!(Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for deployment"
}

# Install frontend dependencies
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

# Deploy to Vercel
Write-Host "🌐 Deploying to Vercel..." -ForegroundColor Green
vercel --prod

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🔗 Your app should be live at the URL shown above" -ForegroundColor Cyan
Write-Host "📝 Don't forget to update the API URL environment variable!" -ForegroundColor Yellow