# Sample-Jenkins-GitHub-integration

This repository demonstrates Jenkins and GitHub integration with automated status checks for pull requests.

## 🚀 Features

- ✅ Automated Jenkins builds on push and pull requests
- ✅ GitHub status checks integration
- ✅ Multi-branch pipeline support
- ✅ PR merge validation

## 📋 Setup

Follow the comprehensive setup guide in [JENKINS_SETUP_GUIDE.md](JENKINS_SETUP_GUIDE.md) to enable Jenkins status checks.

## 🔧 Jenkins Configuration

- **Jenkins URL**: http://172.30.47.147:8090/
- **Repository**: https://github.com/pavan-msys/Sample-Jenkins-GitHub-integration.git

## 📖 Quick Start

1. Install required Jenkins plugins (GitHub, GitHub Branch Source, Pipeline)
2. Configure GitHub credentials in Jenkins
3. Set up webhook in GitHub repository
4. Create Multibranch Pipeline job
5. Test with a pull request

See [JENKINS_SETUP_GUIDE.md](JENKINS_SETUP_GUIDE.md) for detailed instructions.

## 🔄 Status Checks

Once configured, you'll see the following status checks on pull requests:
- `continuous-integration/jenkins/branch` - Branch build status
- `continuous-integration/jenkins/pr-merge` - PR merge validation

## 📝 License

MIT License