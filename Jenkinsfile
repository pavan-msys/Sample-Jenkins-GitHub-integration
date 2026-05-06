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
                bat '''
                    python --version
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building the application...'
                bat 'python -m py_compile app.py'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                bat '''
                    python -m pytest test_app.py -v --junitxml=test-results.xml
                    python -m pytest test_app.py --cov=app --cov-report=html --cov-report=term
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                echo 'Checking code quality...'
                bat 'python app.py'
            }
        }
    }
    
    post {
        always {
            echo 'Archiving test results...'
            junit 'test-results.xml'
            echo 'Publishing HTML reports...'
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        success {
            echo 'Pipeline completed successfully! ✓'
        }
        failure {
            echo 'Pipeline failed! ✗'
        }
    }
}
