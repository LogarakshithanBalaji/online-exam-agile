
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python and Git') {
            steps {
                bat '"C:/Users/Logar/Online-Exam-Agile/venv/Scripts/python.exe" --version'
                bat 'git --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C:/Users/Logar/Online-Exam-Agile/venv/Scripts/python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Automated Tests') {
            steps {
                bat '"C:/Users/Logar/Online-Exam-Agile/venv/Scripts/python.exe" -m pytest -v'
            }
        }
    }
}

