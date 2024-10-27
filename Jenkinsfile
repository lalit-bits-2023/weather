pipeline {
    agent any
    environment {
        // Define docker image name and tag
        def python3 = ' C:\\Users\\lalit\\AppData\\Local\\Microsoft\\WindowsApps\\python'
        python = "C:\\Program Files\\Python313\\python.exe" 
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
                    // Python Path
                    // Capture the Python version output
                    def versionOutput = bat(script: "${python} --version", returnStdout: true).trim()
                    // Extract only the version number using regex
                    def version = versionOutput.replaceAll("Python ", "").trim()
                    echo "Python version: ${version}"
                    //bat "${python} -m pip install -r requirements.txt"
                }
            }
        }
    }
}
