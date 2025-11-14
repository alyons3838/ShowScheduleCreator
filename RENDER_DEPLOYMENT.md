# Deploy to Render - Step by Step Guide

This guide will walk you through deploying the Show Schedule Creator to Render so your team can access it via a URL.

## Prerequisites

- [x] Render account (free tier works!) - ✅ You have this
- [x] GitHub repository with the code - ✅ You have this

## Deployment Steps

### Step 1: Connect GitHub to Render

1. Go to your Render Dashboard: https://dashboard.render.com/
2. Click **"New +"** button in the top right
3. Select **"Web Service"**
4. Click **"Connect GitHub"** (if not already connected)
5. Authorize Render to access your GitHub repositories

### Step 2: Select Your Repository

1. Find **"ShowScheduleCreator"** in the repository list
2. Click **"Connect"**

### Step 3: Configure the Web Service

Fill in these settings:

**Name:** `thousand-hills-schedule-creator` (or whatever you prefer)

**Region:** Choose closest to your team (e.g., `US East (Ohio)`)

**Branch:** `claude/create-app-011CV37UnS7fEFxGB4C7UE1q`

**Root Directory:** (leave blank)

**Runtime:** `Python 3`

**Build Command:**
```
pip install -r requirements-web.txt
```

**Start Command:**
```
gunicorn wsgi:app
```

**Instance Type:** `Free` (should be fine for your needs)

### Step 4: Advanced Settings (Optional but Recommended)

Click **"Advanced"** and add environment variable:

**Key:** `SECRET_KEY`
**Value:** (generate a random string, like: `THV-2024-SecretKey-RandomString123`)

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render will start building your app
3. Wait 3-5 minutes for the build to complete
4. You'll see logs showing the build progress

### Step 6: Get Your URL

Once deployed, Render will give you a URL like:
```
https://thousand-hills-schedule-creator.onrender.com
```

**That's it!** Share this URL with your sales reps.

## Using the App

Your team can now:
1. Visit the URL in any browser
2. Upload PDFs
3. Download branded schedules

**No installation needed!**

## Free Tier Limitations

Render's free tier:
- ✅ **Free forever** for basic apps
- ⚠️ **Spins down after 15 minutes** of inactivity
- ⚠️ **Takes 30-60 seconds** to wake up on first visit after sleeping
- ✅ **Then works normally** until inactive again

**If the slow wake-up bothers you:** Upgrade to paid tier ($7/month) for always-on service.

## Troubleshooting

### Build Failed

**Check the logs** in Render dashboard. Common issues:

1. **"No module named X"** → File is missing from requirements-web.txt
2. **"Port already in use"** → Shouldn't happen on Render, but restart the service

### App Deployed but Won't Load

1. Check **Logs** tab in Render dashboard
2. Look for error messages
3. Make sure start command is: `gunicorn wsgi:app`

### Uploads Failing

Render's free tier has limited storage. Old PDFs will be automatically cleaned up when the server restarts (happens during sleep/wake cycles).

## Updating the App

When you make changes to the code:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

2. **Render auto-deploys** (usually within 1-2 minutes)

3. **Or manually deploy:**
   - Go to Render dashboard
   - Click "Manual Deploy" → "Deploy latest commit"

## Custom Domain (Optional)

Want to use your own domain like `schedules.thousandhills.com`?

1. Go to **Settings** in Render dashboard
2. Click **"Custom Domain"**
3. Add your domain
4. Update DNS records as instructed
5. Free SSL certificate included!

## Monitoring

Check app health:
- Visit: `https://your-app-url.onrender.com/health`
- Should show: `{"status":"healthy","app":"Thousand Hills Show Schedule Creator"}`

## Cost Summary

**Free Tier:**
- Cost: $0/month
- Perfect for occasional use
- Spins down when idle
- Wakes up in ~30-60 seconds

**Paid Tier ($7/month):**
- Always-on (no spin down)
- Faster performance
- 24/7 availability

## Support

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com/

## Next Steps

Once deployed:
1. Test the URL yourself
2. Share with 1-2 reps for testing
3. Roll out to full team
4. Update USER_GUIDE.md with the URL

---

**Questions?** Check Render's excellent documentation or their community forums.
