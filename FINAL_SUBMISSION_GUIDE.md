# 🚀 Final Submission Guide: LegalEase

You have successfully written all the code! Now you just need to get it online and submit it to SkillWallet to secure your 100% completion score. 

Follow these 3 exact steps:

---

## Step 1: Push Your Code to GitHub

I have already initialized the Git repository on your machine. You just need to link it to your GitHub account and push it.

1. Go to your GitHub account (https://github.com/ishwarya123-lab) and create a **New Repository**. Name it `legalease`. (Do not add a README or .gitignore, just create the empty repo).
2. Open your terminal in VS Code (or Command Prompt) inside `F:\123\legalease`.
3. Run these exact commands one by one to configure your team and push the code:

```bash
# 1. Set your name for the commits (Requirement: Team Credits)
git config user.name "ISHWARYA M"
git config user.email "ishwarya@example.com"

# 2. Add all the code
git add .

# 3. Create the final commit
git commit -m "Final Submission: Complete LegalEase AI architecture and implementation"

# 4. Link to your new GitHub repository (replace with your actual URL!)
git remote add origin https://github.com/ishwarya123-lab/legalease.git

# 5. Push the code to the cloud
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy for Free on Render (Live Demo URL)

SkillWallet requires a "Live Hosted Demo URL". The absolute easiest way to deploy this Dockerized FastAPI app for free is using **Render.com**.

1. Go to [Render.com](https://render.com) and sign in with your GitHub account.
2. Click **New +** in the top right and select **Web Service**.
3. Choose **Build and deploy from a Git repository**.
4. Connect the `legalease` repository you just created.
5. In the Render deployment settings, fill this out:
   - **Name**: `legalease-ai`
   - **Environment**: `Docker` (Render will automatically detect your `backend/Dockerfile`!)
   - **Root Directory**: `backend` *(⚠️ Crucial! Make sure you type `backend` here)*
   - **Instance Type**: Free
6. Scroll down to **Environment Variables** and add your Gemini API Key:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: *(Paste your actual Google AI Studio API key here)*
7. Click **Create Web Service**. 

Wait about 3-5 minutes for it to build. Once it says "Live", copy the URL (e.g., `https://legalease-ai.onrender.com`).

---

## Step 3: SkillWallet Submission & 100% Kanban

Now that you have your GitHub URL and your Live Render URL, it's time to get your grade!

1. **Submit Links:** Have **Aafrin** (your Team Lead) log into SkillWallet. At the very top of your project page, there will be an alert banner asking for the links. Aafrin must paste:
   - **GitHub Repository URL**: `https://github.com/ishwarya123-lab/legalease`
   - **Live Hosted Demo URL**: `https://legalease-ai.onrender.com`

2. **Move Kanban to Done:** Go to the **Kanban tab** on your SkillWallet dashboard. 
   - Drag all 14 Tasks from the **"To Do"** or **"In Progress"** columns completely over to the **"Done"** column.
   - Once the last card is dropped in "Done", your progress meter will hit **100%**.

🎉 **Congratulations! You have completed the Google Cloud Generative AI module!**
