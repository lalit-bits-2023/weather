pipeline {
    agent any
    environment {
        // Python Binary Path
        python = '"C:\\Program Files\\Python313\\python.exe"' 
    }

    stages {
        stage('Clone') {
            steps {
                // Cloning GIT Repository
                echo 'Cloning Repository...'
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
            }
        }
        stage('Version') {
            steps {
                script {
                    // Validating Python Version
                    def version = bat(script: "${python} --version", returnStdout: true)

                    version = version.split()[-1]

                    if (version == "3.13.0") {
                        echo "Python Version : ${version} is valid."
                    } else {
                        echo "Python Version : ${version} is not valid."
                    }
                }
            }
        }
    }
}
