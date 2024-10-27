pipeline {
    agent any
    environment {
        // Define docker image name and tag
        def python = ' C:\\Users\\lalit\\AppData\\Local\\Microsoft\\WindowsApps\\python'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning Repository...'
                // Cloning GIT Repository
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Cloning Repository...'
                    // Install dependencies using pip
                    bat '${python} -m pip install -r requirements.txt'
                }
            }
        }
    }
}
