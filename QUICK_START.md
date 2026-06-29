# Quick Start Checklist

## ✅ 5-Minute Setup (Do These in Order)

### 1. Download Your Site
- Click "Files" icon in Abacus AI (top right)
- Download the `musicofthe70s` folder
- Extract ZIP to your computer

### 2. Create GitHub Account & Repo
- Sign up: https://github.com/signup
- Create new repository: `musicofthe70s` (public)
- Don't add README

### 3. Push to GitHub
**Easiest method:** Download GitHub Desktop
- https://desktop.github.com/
- Sign in → Add Local Repository → Select your folder
- Click "Publish repository"

**OR use command line:**
```bash
cd /path/to/musicofthe70s
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/musicofthe70s.git
git branch -M main
git push -u origin main
```
(Need a Personal Access Token, not password: https://github.com/settings/tokens)

### 4. Deploy to Cloudflare Pages
- Sign up: https://dash.cloudflare.com/sign-up
- Go to "Workers & Pages" → "Create" → "Pages" → "Connect to Git"
- Connect GitHub → Select `musicofthe70s` repo
- Build settings: Framework = None, Build command = empty, Output = `/`
- Click "Save and Deploy"
- **Your site is live at:** `https://musicofthe70s.pages.dev`

### 5. Buy & Connect Domain
**Option A - Cloudflare (recommended, ~$9/year):**
- In Cloudflare: "Domain Registration" → Search `musicofthe70s.net`
- Purchase domain
- Go to "Workers & Pages" → Your project → "Custom domains"
- Add `musicofthe70s.net` (auto-configures DNS)
- Add `www.musicofthe70s.net`

**Option B - Namecheap (~$12/year):**
- Buy at https://namecheap.com
- In Namecheap: Domain List → Manage → Nameservers → Custom DNS
- In Cloudflare: "Websites" → "Add site" → Enter your domain
- Copy Cloudflare's 2 nameservers to Namecheap
- Wait 1-24 hours for propagation
- In Cloudflare: "Workers & Pages" → Custom domains → Add your domain

---

## 📋 What You Get

- **Live site:** `https://musicofthe70s.net` (after domain connects)
- **Free hosting:** 100,000 requests/month
- **Auto-deploy:** Every GitHub push updates the site in ~1 minute
- **HTTPS:** Automatic SSL certificate
- **CDN:** Global fast loading

---

## 🔄 Making Updates Later

1. Edit files on your computer
2. **GitHub Desktop:** Commit + Push
   **OR Command Line:** `git add . && git commit -m "Update" && git push`
3. Cloudflare auto-deploys in ~60 seconds

---

## 📞 Get Help

Full detailed guide: See `DEPLOYMENT_GUIDE.md` (or the PDF/Word versions)

---

**Total Time:** 15-20 minutes (plus domain propagation wait)
**Total Cost:** ~$9-15/year (just the domain)
