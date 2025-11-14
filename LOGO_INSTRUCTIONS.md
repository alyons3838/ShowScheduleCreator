# Adding Your Logo

To add the Thousand Hills Vacations logo to branded PDFs:

## Step 1: Get Your Logo File

You need a logo image file in one of these formats:
- PNG (recommended - supports transparency)
- JPG/JPEG
- GIF

## Step 2: Prepare the Logo

**Recommended specs:**
- Width: 800-1200 pixels
- Format: PNG with transparent background
- Aspect ratio: Preserve original (will scale proportionally)

## Step 3: Upload to Render

### If You Have the Code Locally:

1. Save your logo as `logo.png`
2. Place it in the `static/` folder
3. Commit and push:
   ```bash
   git add static/logo.png
   git commit -m "Add Thousand Hills Vacations logo"
   git push
   ```
4. Render will auto-deploy with the logo

### If You're Using Render Directly:

Unfortunately, Render doesn't have a file upload feature for deployed apps. You have two options:

**Option A: Add to GitHub**
1. Go to your GitHub repository
2. Navigate to the `static` folder
3. Click "Add file" → "Upload files"
4. Upload your `logo.png`
5. Commit the change
6. Render will auto-deploy

**Option B: Use an Image URL**
If you have the logo hosted somewhere (your website, cloud storage, etc.), I can modify the code to fetch it from a URL instead.

## Step 4: Test

After deploying:
1. Upload a PDF to the app
2. Check the branded output
3. Logo should appear centered at the top

## Logo Not Showing?

**Check these:**

1. **File name** - Must be exactly `logo.png` (lowercase)
2. **Location** - Must be in the `static/` folder
3. **Format** - PNG, JPG, or GIF
4. **Deployment** - Make sure Render deployed the latest version

## Need Help?

If you can't add the logo yourself:
1. Email the logo file to your developer/IT person
2. They can add it to the repository and push
3. Or let me know and I can help modify the approach

---

**Note:** The logo will appear at ~2.5 inches wide and scale proportionally. If you want a different size, I can adjust that.
