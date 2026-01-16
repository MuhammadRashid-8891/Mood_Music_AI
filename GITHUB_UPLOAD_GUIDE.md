# How to Upload Your Project to GitHub

You have successfully initialized your project with Git and committed your files locally. The only step left is to send this to GitHub.

## Step 1: Create a Repository on GitHub
1. Go to [GitHub.com](https://github.com/) and log in.
2. Click the **+** icon in the top-right corner and select **New repository**.
3. **Repository name**: Enter `Mood_Music_AI` (or any name you prefer).
4. **Description**: (Optional) "An AI-powered music playlist generator."
5. **Public/Private**: Choose whichever you prefer.
6. **Initialize this repository with**: DO NOT check any of these boxes (Add a README file, .gitignore, license). We already have these!
7. Click **Create repository**.

## Step 2: Push Your Code
Once the repository is created, GitHub will show you a page with setup commands. Look for the section **"…or push an existing repository from the command line"**.

Copy the commands shown there. They will look like this:

```bash
git remote add origin https://github.com/YOUR_USERNAME/Mood_Music_AI.git
git push -u origin main
```

## Step 3: Run the Commands
1. Open your terminal in VS Code (Ctrl+`).
2. Paste the commands you copied and hit Enter.
3. If this is your first time, it may ask you to sign in to GitHub. Follow the browser prompt.

## Success!
Once done, refresh your GitHub repository page. You should see all your files, including your `README.md` beautifully rendered!
