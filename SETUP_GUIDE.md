# Jenkins-GitHub Integration Setup Guide

This guide will help you set up Jenkins to automatically build and test Pull Requests with status checks that block merging on test failures.

## 📋 Prerequisites

- Jenkins server running (example: http://172.30.47.147:8090/)
- GitHub repository (example: https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration)
- Admin access to both Jenkins and GitHub repository

---

## 🎯 What You'll Achieve

- ✅ Automatic builds on every push and pull request
- ✅ Status checks displayed on GitHub PRs
- ✅ Merge blocking when tests fail
- ✅ Green checkmark when tests pass

---

## Step 1: Install Jenkins Plugins

1. Go to Jenkins → **Manage Jenkins** → **Manage Plugins**
2. Click **Available** tab
3. Search and install these plugins:
   - **GitHub Plugin**
   - **GitHub Branch Source Plugin**
   - **Pipeline Plugin**
   - **Git Plugin**
4. Click **Install without restart** (or restart if needed)

---

## Step 2: Create GitHub Personal Access Token

1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token (classic)**
3. Configure:
   - **Note**: `Jenkins Integration`
   - **Expiration**: Choose appropriate duration
   - **Select scopes**:
     - ✅ **`repo`** (Full control - includes repo:status) **← CRITICAL**
     - ✅ **`admin:repo_hook`** (Write repository hooks)
4. Click **Generate token**
5. **COPY THE TOKEN** - you won't see it again!

---

## Step 3: Add GitHub Credentials to Jenkins

1. Go to Jenkins → **Manage Jenkins** → **Manage Credentials**
2. Click **(global)** domain
3. Click **Add Credentials**
4. Configure:
   - **Kind**: `Username with password`
   - **Username**: Your GitHub username (e.g., `pavan-msys`)
   - **Password**: Paste the GitHub Personal Access Token
   - **ID**: `github-token` (or any memorable name)
   - **Description**: `GitHub PAT for CI/CD`
5. Click **Create**

---

## Step 4: Create Jenkinsfile in Repository

Create a file named `Jenkinsfile` in your repository root:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Code checked out successfully'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 --version || python --version
                    pip3 install -r requirements.txt || pip install -r requirements.txt
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh 'python3 -m py_compile app.py || python -m py_compile app.py'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    python3 -m pytest test_app.py -v --junitxml=test-results.xml || python -m pytest test_app.py -v --junitxml=test-results.xml
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Archiving test results...'
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
        success {
            echo 'Pipeline completed successfully! ✓'
        }
        failure {
            echo 'Pipeline failed! ✗'
        }
    }
}
```

**Note**: 
- Use `sh` for Linux/Mac agents
- Use `bat` for Windows agents
- Adjust commands for your tech stack (Node.js, Java, etc.)

---

## Step 5: Create Multibranch Pipeline in Jenkins

1. Go to Jenkins Dashboard → **New Item**
2. Enter name: `Your-Repo-Name` (e.g., `Sample-Jenkins-GitHub-integration`)
3. Select **Multibranch Pipeline**
4. Click **OK**
5. Configure:

### Branch Sources:
- Click **Add source** → **GitHub**
- **Credentials**: Select the credential you created (e.g., `github-token`)
- **Repository HTTPS URL**: `https://github.com/your-username/your-repo`
  - OR use separate fields:
    - **Owner**: `your-username`
    - **Repository**: `your-repo-name`

### Behaviors:
The following should be added by default, verify they exist:
- ✅ **Discover branches**
  - Strategy: `Exclude branches that are also filed as PRs`
- ✅ **Discover pull requests from origin**
  - Strategy: `Merging the pull request with the current target branch revision`
- ✅ **Discover pull requests from forks**
  - Strategy: `Merging the pull request with the current target branch revision`
  - Trust: `From users with Admin or Write permission`

### Build Configuration:
- **Mode**: `by Jenkinsfile`
- **Script Path**: `Jenkinsfile`

### Scan Multibranch Pipeline Triggers:
- ⬜ **Periodically if not otherwise run** - UNCHECK THIS (we'll use webhooks instead)

6. Click **Save**
7. Jenkins will automatically scan the repository and discover branches/PRs

**If you already created the job with periodic scanning enabled:**
1. Go to the job → **Configure**
2. Scroll to **"Scan Multibranch Pipeline Triggers"**
3. **UNCHECK** "Periodically if not otherwise run"
4. Click **Save**

---

## Step 6: Expose Jenkins for Webhooks (Required for Private Jenkins)

**If your Jenkins is on a private IP** (like `172.30.47.147`), GitHub cannot reach it directly. You need to expose it using ngrok:

### Install and Setup ngrok:

1. **Download ngrok**: https://ngrok.com/download
   - Or use command:
   ```powershell
   # Download and extract
   Invoke-WebRequest -Uri "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip" -OutFile "ngrok.zip"
   Expand-Archive ngrok.zip -DestinationPath .
   ```

2. **Sign up for free account** (optional but recommended for longer sessions)
   - Go to https://dashboard.ngrok.com/signup
   - Get your authtoken
   - Run: `ngrok config add-authtoken YOUR_TOKEN`

3. **Start ngrok tunnel**:
   ```powershell
   .\ngrok http 8090
   ```

4. **Copy the public URL** from ngrok output:
   ```
   Forwarding   https://abc123-xyz.ngrok-free.app -> http://172.30.47.147:8090
   ```
   Copy the `https://abc123-xyz.ngrok-free.app` URL

**Keep ngrok running** - Don't close this terminal window!

**If Jenkins is already publicly accessible**, skip to Step 7.

---

## Step 7: Configure GitHub Webhook (Required)

**This is CRITICAL for instant builds on push/PR events.**

1. Go to your GitHub repository → **Settings** → **Webhooks** → **Add webhook**
2. Configure:
   - **Payload URL**: `https://your-jenkins-url/github-webhook/`
     - If using ngrok: `https://abc123-xyz.ngrok-free.app/github-webhook/`
     - If public Jenkins: `http://your-public-ip:8090/github-webhook/`
   - **Content type**: `application/json`
   - **Which events?**: Select **Let me select individual events**
     - ✅ `Pushes`
     - ✅ `Pull requests`
   - ✅ **Active**
3. Click **Add webhook**
4. **Verify**: You should see a green checkmark after the first event

**Important**: 
- Webhook URL must end with `/github-webhook/`
- Use HTTPS when using ngrok
- Keep ngrok running at all times for webhooks to work

---

## Step 8: Set Up Branch Protection Rules

1. Go to your GitHub repository → **Settings** → **Branches**
2. Click **Add branch protection rule**
3. Configure:
   - **Branch name pattern**: `main` (or your default branch)
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - In the search box, type and add **ONLY** these checks for PRs:
     - ✅ `continuous-integration/jenkins/pr-merge` **← Required for PRs**
     - ✅ `continuous-integration/jenkins/pr-head` (optional, add if it appears)
   
   **Important Notes**: 
   - **DO NOT add** `continuous-integration/jenkins/branch` - it's for direct branch commits, not PRs
   - Only add checks that actually appear on your PRs
   - Check names only appear after Jenkins posts them at least once
   - You can type them manually if needed

4. Optional but recommended:
   - ✅ **Require a pull request before merging**
   - **Required approvals**: 1

5. Click **Create** or **Save changes**

---

## Step 9: Test the Setup

### Test 1: Create a Pull Request

1. Create a new branch:
   ```bash
   git checkout -b test-jenkins
   ```

2. Make a change to any file:
   ```bash
   echo "Testing Jenkins" >> README.md
   git add README.md
   git commit -m "Test Jenkins integration"
   git push origin test-jenkins
   ```

3. Go to GitHub and create a Pull Request

4. **Expected Results**:
   - Jenkins **instantly** starts building (via webhook)
   - Status checks appear on the PR immediately
   - If tests pass: Green checkmark ✅
   - Merge button is enabled

### Test 2: Verify Test Failure Blocks Merge

1. Intentionally break a test in your test file
2. Commit and push to the same PR branch
3. **Expected Results**:
   - Jenkins builds and tests fail
   - Status check shows red X ❌
   - **Merge button is DISABLED/BLOCKED** 🚫
   - Cannot merge until tests are fixed

### Test 3: Fix and Verify Merge Enabled

1. Fix the broken test
2. Commit and push
3. **Expected Results**:
   - Jenkins builds and tests pass
   - Status check shows green checkmark ✅
   - **Merge button is ENABLED** ✅
   - Can merge the PR

---

## 🔍 Troubleshooting

### Issue: "Could not update commit status - 403"

**Cause**: GitHub token missing `repo:status` permission

**Solution**:
1. Regenerate GitHub token with full `repo` scope
2. Update Jenkins credential with new token
3. Trigger rebuild

### Issue: Status checks not appearing on PR

**Cause**: 
- Token permissions issue
- Jenkins can't reach GitHub
- Job not configured correctly

**Solution**:
1. Check Jenkins build logs for errors
2. Verify token has `repo` permission
3. Ensure Jenkinsfile exists in repository
4. Check Jenkins job configuration

### Issue: Webhook shows "never been triggered"

**Cause**: 
- Jenkins on private IP - GitHub can't reach it
- ngrok not running
- Wrong webhook URL

**Solution**:
1. **Verify ngrok is running** - Check the ngrok terminal window
2. **Check webhook URL** - Must match current ngrok URL exactly
3. **Restart ngrok** if URL changed (free tier gets new URL on restart):
   ```powershell
   ngrok http 8090
   ```
4. **Update GitHub webhook** with new ngrok URL
5. **Test delivery** - Go to GitHub webhook settings → Recent Deliveries → Redeliver

**Note**: With free ngrok, URL changes when you restart. Use paid plan for permanent URL or keep ngrok running 24/7.

### Issue: Merge button not blocked on test failure

**Cause**: 
- Branch protection not configured
- Wrong status check names in branch protection

**Solution**:
1. Verify branch protection is active
2. Add the exact check names that Jenkins posts:
   - Check your PR to see exact check names
   - Add those exact names to branch protection

### Issue: Build fails with "batch scripts can only be run on Windows"

**Cause**: Using `bat` commands on Linux agent

**Solution**: Use `sh` instead of `bat` in Jenkinsfile (or vice versa for Windows)

### Issue: Builds taking too long to start (delay of minutes)

**Cause**: Using periodic scanning instead of webhooks

**Solution**:
1. Verify ngrok is running
2. Check webhook is configured in GitHub
3. Test webhook: GitHub → Settings → Webhooks → Recent Deliveries
4. If webhook failing, update with current ngrok URL
5. **With webhooks, builds start in seconds, not minutes**

### Issue: Some checks stuck on "Expected - Waiting for status"

**Cause**: Branch protection requiring wrong status checks for PRs

**Solution**:
1. Check which status checks Jenkins **actually posted** on your PR
2. Go to branch protection settings
3. **Remove** any checks that show "Expected - Waiting" (like `continuous-integration/jenkins/branch`)
4. **Only require** checks that Jenkins actually posts to PRs:
   - `continuous-integration/jenkins/pr-merge` ✅
   - `continuous-integration/jenkins/pr-head` (if it appears)
5. Save and refresh PR

**Explanation**: 
- `jenkins/branch` = for direct branch commits
- `jenkins/pr-merge` = for pull requests ✅
- Only require checks that apply to PRs!

---

## 📊 Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   GitHub    │         │   ngrok      │         │   Jenkins   │         ┌─────────────┐
│  Repository │────────►│   Tunnel     │────────►│   Server    │────────►│   Tests     │
└─────────────┘         └──────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │                        │
      │                        │                        │                        │
      ▼                        ▼                        ▼                        ▼
  1. Push/PR           2. Webhook POST          3. Trigger build          4. Run Tests
  (instant)            to ngrok URL             (instant start)           (pass/fail)
                                                        │
                                                        ▼
                                                 5. Post status
                                                    to GitHub
                                                        │
                                                        ▼
                                              6. Update PR status
                                                (enable/block merge)
```

**Flow**:
1. Developer pushes code or creates PR
2. GitHub **instantly** sends webhook to ngrok URL
3. ngrok forwards to Jenkins (on private IP)
4. Jenkins triggers build immediately
5. Tests run and results are posted back to GitHub
6. PR shows status checks and merge button state updates

---

## 🎯 Best Practices

1. **Keep ngrok running** - Required for webhooks with private Jenkins (or use paid plan for permanent URL)
2. **Use meaningful commit messages** - They appear in Jenkins builds
3. **Keep Jenkinsfile in version control** - Track changes to CI/CD pipeline
4. **Run tests locally first** - Before pushing to avoid failing builds
5. **Monitor webhook deliveries** - Check GitHub webhook page for failed deliveries
6. **Secure Jenkins** - Use authentication and HTTPS in production
7. **Review build logs** - Understand failures before fixing code
8. **Update token expiration** - Set calendar reminders for token renewal

---

## 📚 Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [GitHub Webhooks Guide](https://docs.github.com/en/webhooks)
- [GitHub Status Checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

## ✅ Success Checklist

- [ ] Jenkins plugins installed
- [ ] GitHub Personal Access Token created with `repo` scope
- [ ] Credentials added to Jenkins
- [ ] Jenkinsfile created in repository
- [ ] Multibranch Pipeline job created and configured
- [ ] **ngrok installed and running** (if Jenkins is on private IP)
- [ ] GitHub webhook configured with ngrok/public URL
- [ ] **Webhook tested and showing green checkmark**
- [ ] Branch protection rules enabled with required status checks
- [ ] Test PR created and status checks appear **instantly**
- [ ] Failed test blocks merge ❌
- [ ] Passed test allows merge ✅

---

**Congratulations! 🎉** You now have a complete Jenkins-GitHub CI/CD pipeline with **instant webhook-triggered builds**, automated testing, and merge protection!
