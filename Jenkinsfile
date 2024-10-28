pipeline {
    agent any
    environment {
        // Python Binary Path
        python = '"C:\\Program Files\\Python313\\python.exe"'
        PYTHONPATH = '"C:\\Users\\lalit\\Desktop\\projects\\weather"'
    }

    stages {
        //stage('Clone Repository') {
        //    steps {
        //    // Cloning GIT Repository
        //        echo 'Cloning Repository...'
        //        git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
        //    }
        //}
        stage('Check Python Version') {
            steps {
                script {
                    // Checking python version
                    echo "Checking Python Version..."
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
        stage('Install Dependencies') {
            steps {
                script {
                    // Install project dependencies using pip
                    echo 'Installaing Dependencies...'
                    bat "${python} -m pip install -r requirements.txt"
                }
            }
        }
        stage('Launch Application') {
            steps {
                script {
                    // Launch GUI (Tkinter) application
                    echo 'Launching Application...'
                    //Use 'start' to run the Python application in a non-blocking way
                    bat(script: "start ${python} app\\main.py", returnStatus: true)
                    // Use 'start /B' to run the Python application in the background
                    //bat(script: "start /B ${python} main.py", returnStatus: true)
                }
            }
        }
        stage('Run Unit Tests') {
            steps {
                script {
                    // Run Unit Testcases
                    echo 'Running Unit Testcases for main.py'
                    bat "${python} -m unittest test.test_main"
                    echo 'Running Unit Testcases for ui.py'
                    bat "${python} -m unittest test.test_ui"
                    echo 'Running Unit Testcases for weather.py'
                    bat "${python} -m unittest test.test_weather"
                }
            }
        }
    }
}
