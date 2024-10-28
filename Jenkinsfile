pipeline {
    agent any
    environment {
        // Python Binary Path
        python = '"C:\\Program Files\\Python313\\python.exe"'
        PYTHONPATH = '"C:\\Users\\lalit\\Desktop\\projects\\weather"'
        def imageName = 'lalitbits2023/weather'
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
                    //echo 'Running Unit Testcases for ui.py'
                    //bat "${python} -m unittest test.test_ui"
                    //echo 'Running Unit Testcases for weather.py'
                    //bat "${python} -m unittest test.test_weather"
                }
            }
        }
        stage('Create Docker Image') {
            steps {
                script {
                    imageTag = 1
                    while (true) {
                        def response = bat (
                            script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/v${imageTag}",
                            returnStdout: true
                        ).trim()

                        response = response.split()[-1]

                        if (response == "200") {
                            echo "Image version ${imageName}:v${imageTag} exists on Docker Hub."
                            imageTag += 1
                        } else if (response == "404") {
                            echo "Image version ${imageName}:v${imageTag} does not exist on Docker Hub."
                            echo "Next Image version should be ${imageName}:v${imageTag}."
                            break
                        } else {
                            echo "Error checking image version. HTTP Status: ${response}"
                        }
                    }

                    sleep(time: 2, unit: 'SECONDS') // Sleep for 2 minute
                    // Build the docker image from the dockerfile present in the current workspace
                    echo "Building Docker Image ${imageName}:v${imageTag}"
                    dockerImage = docker.build("${imageName}:v${imageTag}")
                    echo "Docker Image ${imageName}:${imageTag} built successfully."

                    sleep(time: 2, unit: 'SECONDS') // Sleep for 2 minute
                    // Push the docker to DockerHub
                    echo "Pushing Docker Image on DockerHub"
                    docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                        dockerImage.push()
                    }
                    echo "Docker Images pushed successfully."
                    sleep(time: 2, unit: 'SECONDS') // Sleep for 2 minute
                }
            }
        }

    }
}
