pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'clone....'
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/notepad.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                // Your build steps here
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                // Your test steps here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Your deploy steps here
            }
        }
    }
}
