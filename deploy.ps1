# ============================================================
#  Egypt Jobs AI — Auto GitHub Push Script
#  انقر بزر الفأرة الأيمن على هذا الملف واختر "Run with PowerShell"
# ============================================================

$projectPath = "c:\Users\ftyyr\Downloads\stitch_mazaya_smart_life_ecosystem\Egypt-Jobs-AI"
$repoUrl     = "https://github.com/shahd-shaban88/Egypt-Jobs-AI.git"
$authorName  = "Shahd Shaban"
$authorEmail = "shahd.shaban88@gmail.com"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   Egypt Jobs AI — Deploying to GitHub  " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location $projectPath

# Init git
Write-Host "[1/6] Initializing Git..." -ForegroundColor Yellow
git init

# Set author identity
Write-Host "[2/6] Setting author identity..." -ForegroundColor Yellow
git config user.name  $authorName
git config user.email $authorEmail

# Add remote (remove old if exists)
Write-Host "[3/6] Setting remote origin..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin $repoUrl

# Stage all files
Write-Host "[4/6] Staging all files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "[5/6] Creating first commit..." -ForegroundColor Yellow
git commit -m "feat: initial launch of Egypt Jobs AI platform"

# Push
Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main --force

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " SUCCESS! Now enable GitHub Pages:       " -ForegroundColor Green
Write-Host " 1. Go to: github.com/shahd-shaban88/Egypt-Jobs-AI/settings/pages" -ForegroundColor Green
Write-Host " 2. Branch: main  /  Folder: / (root)   " -ForegroundColor Green
Write-Host " 3. Click Save                           " -ForegroundColor Green
Write-Host " Site will be live at:                   " -ForegroundColor Green
Write-Host " https://shahd-shaban88.github.io/Egypt-Jobs-AI" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
