pipeline {
    agent any
    environment {
        // Define docker image name and tag
        def python3 = ' C:\\Users\\lalit\\AppData\\Local\\Microsoft\\WindowsApps\\python'
        python = '"C:\\Program Files\\Python313\\python.exe"' 
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
                    //def python = '"C:\\Program Files\\Python313\\python"'
                    // Valiadting Python Version
                    // Capture the output of the Python version command
                    def version = bat(script: "${python} --version", returnStdout: true)
                    version = version.split()[-1]
                    echo ">>${version}<<"
                    // Install dependencies using pip
                    //bat "${python} -m pip install -r requirements.txt"
                }
            }
        }
    }
}
