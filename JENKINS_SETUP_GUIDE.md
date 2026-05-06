# Jenkins GitHub Status Checks Setup Guide

This guide will help you enable Jenkins status checks in your GitHub repository to display build status like in the screenshot.

## Prerequisites
- Jenkins server running at: `http://172.30.47.147:8090/`
- GitHub repository: `https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration.git`
- Admin access to both Jenkins and GitHub repository

## Step 1: Install Required Jenkins Plugins

1. Go to Jenkins Dashboard → **Manage Jenkins** → **Manage Plugins**
2. Install the following plugins:
   - **GitHub Plugin** (for GitHub integration)
   - **GitHub Branch Source Plugin** (for multi-branch pipelines)
   - **GitHub Authentication Plugin** (for authentication)
   - **Pipeline Plugin** (for Jenkinsfile support)
   - **Git Plugin** (for Git operations)

3. Restart Jenkins after installation:
   ```
   http://172.30.47.147:8090/restart
   ```

## Step 2: Create GitHub Personal Access Token

1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token** (classic)
3. Configure the token:
   - **Note**: `Jenkins Integration Token`
   - **Expiration**: Choose appropriate expiration
   - **Scopes**: Select the following:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `admin:repo_hook` (Write repository hooks)
     - ✅ `admin:org_hook` (if using organization)
4. Click **Generate token** and **COPY THE TOKEN** (you won't see it again!)

## Step 3: Configure GitHub Credentials in Jenkins

1. Go to Jenkins Dashboard → **Manage Jenkins** → **Manage Credentials**
2. Click on **(global)** domain
3. Click **Add Credentials**
4. Configure:
   - **Kind**: `Secret text`
   - **Scope**: `Global`
   - **Secret**: Paste your GitHub Personal Access Token
   - **ID**: `github-token`
   - **Description**: `GitHub Personal Access Token`
5. Click **Create**

## Step 4: Configure GitHub Server in Jenkins

1. Go to **Manage Jenkins** → **Configure System**
2. Scroll to **GitHub** section
3. Click **Add GitHub Server** → **GitHub Server**
4. Configure:
   - **Name**: `GitHub`
   - **API URL**: `https://api.github.com` (default)
   - **Credentials**: Select the `github-token` you created
   - ✅ Check **Manage hooks**
5. Click **Test connection** to verify
6. Click **Save**

## Step 5: Set Up GitHub Webhook

1. Go to your GitHub repository: `https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration`
2. Navigate to **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL**: `http://172.30.47.147:8090/github-webhook/`
   - **Content type**: `application/json`
   - **Secret**: Leave empty (or add if you want additional security)
   - **Which events would you like to trigger this webhook?**
     - ✅ Select **Let me select individual events**
     - ✅ Check: `Pull requests`, `Pushes`, `Pull request reviews`
   - ✅ **Active**: Checked
4. Click **Add webhook**

**Important**: If your Jenkins server is not publicly accessible (172.30.47.147 is a private IP), you'll need to:
- Expose Jenkins through a public URL, OR
- Use a webhook relay service like ngrok, OR
- Use GitHub Enterprise on your network

## Step 6: Create Jenkins Pipeline Job

### Option A: Multibranch Pipeline (Recommended for PR checks)

1. Go to Jenkins Dashboard → **New Item**
2. Enter name: `Sample-Jenkins-GitHub-integration`
3. Select **Multibranch Pipeline**
4. Click **OK**
5. Configure:
   
   **Branch Sources:**
   - Click **Add source** → **GitHub**
   - **Credentials**: Select `github-token`
   - **Repository HTTPS URL**: `https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration`
   - **Behaviors**: 
     - Add **Discover branches**
     - Add **Discover pull requests from origin**
       - Strategy: `Merging the pull request with the current target branch revision`
     - Add **Discover pull requests from forks**
       - Strategy: `Merging the pull request with the current target branch revision`
       - Trust: `From users with Admin or Write permission`
   
   **Build Configuration:**
   - **Mode**: `by Jenkinsfile`
   - **Script Path**: `Jenkinsfile`
   
   **Scan Multibranch Pipeline Triggers:**
   - ✅ Check **Periodically if not otherwise run**
   - **Interval**: `1 minute`

6. Click **Save**
7. Click **Scan Multibranch Pipeline Now**

### Option B: Pipeline Job (For single branch)

1. Go to Jenkins Dashboard → **New Item**
2. Enter name: `Sample-Jenkins-GitHub-integration`
3. Select **Pipeline**
4. Click **OK**
5. Configure:
   
   **General:**
   - ✅ **GitHub project**: `https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration/`
   
   **Build Triggers:**
   - ✅ **GitHub hook trigger for GITScm polling**
   
   **Pipeline:**
   - **Definition**: `Pipeline script from SCM`
   - **SCM**: `Git`
   - **Repository URL**: `https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration.git`
   - **Credentials**: Select `github-token`
   - **Branches to build**: `*/main` (or your default branch)
   - **Script Path**: `Jenkinsfile`

6. Click **Save**

## Step 7: Enable GitHub Status Notifications

The GitHub plugin automatically sends status updates when:
1. Build starts → **In Progress**
2. Build succeeds → **Success** ✅
3. Build fails → **Failure** ❌

These appear as:
- `continuous-integration/jenkins/branch` - For branch builds
- `continuous-integration/jenkins/pr-merge` - For PR merge validation

## Step 8: Test the Integration

1. **Create a Pull Request**:
   ```bash
   git checkout -b test-jenkins-integration
   echo "Testing Jenkins integration" >> README.md
   git add README.md
   git commit -m "Test Jenkins status checks"
   git push origin test-jenkins-integration
   ```

2. **Create PR on GitHub**:
   - Go to your repository on GitHub
   - Click **Pull requests** → **New pull request**
   - Select `test-jenkins-integration` branch
   - Create the pull request

3. **Verify Status Checks**:
   - You should see Jenkins status checks appear on the PR
   - Status should update as build progresses
   - Similar to the screenshot you provided

## Step 9: Configure Branch Protection (Optional)

To require Jenkins checks before merging:

1. Go to GitHub repository → **Settings** → **Branches**
2. Click **Add rule** under Branch protection rules
3. Configure:
   - **Branch name pattern**: `main` (or your default branch)
   - ✅ **Require status checks to pass before merging**
   - ✅ Select: `continuous-integration/jenkins/branch`
   - ✅ Select: `continuous-integration/jenkins/pr-merge`
   - ✅ **Require branches to be up to date before merging**
4. Click **Create** or **Save changes**

## Troubleshooting

### Status checks not appearing?

1. **Check Jenkins logs**:
   - Go to the build in Jenkins
   - Check **Console Output** for errors

2. **Verify GitHub credentials**:
   - Jenkins → Manage Jenkins → Configure System → GitHub
   - Test the connection

3. **Check webhook delivery**:
   - GitHub → Repository → Settings → Webhooks
   - Click on your webhook → Recent Deliveries
   - Check for successful deliveries (green checkmark)

4. **Network connectivity**:
   - Ensure Jenkins can reach GitHub API
   - Ensure GitHub can reach Jenkins webhook endpoint

### Private IP Issue (172.30.47.147)

If Jenkins is on a private network:
- **Option 1**: Use ngrok to create a public tunnel
  ```bash
  ngrok http 8090
  ```
  Then use the ngrok URL for webhook

- **Option 2**: Use GitHub Enterprise on your network

- **Option 3**: Set up Jenkins on a publicly accessible server

## Additional Configuration

### Customize Status Context

In your Jenkinsfile, you can customize status messages:

```groovy
pipeline {
    agent any
    
    options {
        // Set GitHub commit status context
        githubProjectProperty(projectUrlStr: 'https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration')
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    // Set custom GitHub status
                    setBuildStatus("Build", "IN_PROGRESS", "Building...")
                }
                // Your build steps
            }
        }
    }
}

def setBuildStatus(String context, String state, String message) {
    step([
        $class: 'GitHubCommitStatusSetter',
        contextSource: [$class: 'ManuallyEnteredCommitContextSource', context: context],
        statusResultSource: [$class: 'ConditionalStatusResultSource', results: [
            [$class: 'AnyBuildResult', message: message, state: state]
        ]]
    ])
}
```

## Verification Checklist

- [ ] Jenkins plugins installed
- [ ] GitHub Personal Access Token created
- [ ] Credentials configured in Jenkins
- [ ] GitHub Server configured in Jenkins
- [ ] Webhook configured in GitHub
- [ ] Multibranch Pipeline job created
- [ ] Jenkinsfile committed to repository
- [ ] Test PR created
- [ ] Status checks appearing on PR
- [ ] Branch protection configured (optional)

## Support

For issues, check:
- Jenkins logs: `http://172.30.47.147:8090/log/all`
- GitHub webhook deliveries
- Network connectivity between Jenkins and GitHub
