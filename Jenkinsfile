pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                echo 'clone....'
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
            }
        }
    }
}
