pipeline {
    agent any
    
    options {
        quietPeriod(5)  // Wait 5 seconds after webhook trigger to avoid race condition
    }
    
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
                    python3 -m pytest test_app.py --cov=app --cov-report=html --cov-report=term || python -m pytest test_app.py --cov=app --cov-report=html --cov-report=term
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                echo 'Checking code quality...'
                sh 'python3 app.py || python app.py'
            }
        }
    }
    
    post {
        always {
            echo 'Archiving test results...'
            junit allowEmptyResults: true, testResults: 'test-results.xml'
            echo 'Publishing HTML reports...'
            publishHTML([
                allowMissing: true,
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
