pipeline {
    agent any
    environment {
        // Python Binary Path
        python = '"C:\\Program Files\\Python313\\python.exe"'
        python_version = '3.13.0' 
        unitTestcaseList = "unittestcase.txt"
        integrationTestcaseList = "integrationtestcase.txt" 
        def imageName = 'lalitbits2023/weather'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Cloning GIT Repository
                echo 'Cloning Repository...'
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
            }
        }
        stage('Check Python Version') {
            steps {
                script {
                    // Checking python version
                    echo "Checking Python Version..."

                    def version = bat(script: "${python} --version", returnStdout: true)
                    version = version.split()[-1]

                    if (version == "${python_version}") {
                        echo "Python Version : ${version} is correct."
                    } else {
                        error "Python Version : ${version} is not correct."
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    // Install project dependencies using pip
                    echo 'Installaing Dependencies...'

                    def status = bat(script: "${python} -m pip install -r requirements.txt", returnStatus: true)

                    if (status == 0) {
                        echo "Dependencies installed successfully."
                    } else {
                        error "Failed to install dependencies."
                    }
                }
            }
        }
        stage('Unit Tests') {
            steps {
                script {
                    // Running Unit Testcases
                    echo 'Runing Unit Testcases)...'

                    // Reading Unit Testcase File
                    def testCases = readFile(unitTestcaseList).trim().split('\n')

                    for (testCase in testCases) {
                        echo "Running Unit Testcase : ${testCase}"
                        def status = bat(script: "${python} -m unittest test.${testCase}", returnStatus: true)
                        if (status != 0) { 
                            error "Unit testcases '${testcase}' failed."
                        }
                    }
                }
            }
        }
        stage('Integration Tests') {
            steps {
                script {
                    // Running Integration Testcases
                    echo 'Runing Integration Testcases)...'

                    // Reading Integration Testcase File
                    def testCases = readFile(integrationTestcaseList).trim().split('\n')

                    for (testCase in testCases) {
                        echo "Running Integration Testcase : ${testCase}"
                        def status = bat(script: "${python} -m unittest test.${testCase}", returnStatus: true)
                        if (status != 0) { 
                            error "Interation testcases '${testcase}' failed."
                        }
                    }
                }
            }
        }
        stage('Prepare Environment') {
            steps {
                script {
                    // Run a Docker command and capture the exit status
                    def status = bat(script: "docker info", returnStatus: true)
                    
                    // Check if the Docker daemon is running
                    if (status == 0) {
                        echo "Docker daemon is up and running."
                    } else {
                        error "Docker daemon is not running. Please start Docker and try again."
                    }

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
                            echo "Next Image version '${imageName}:v${imageTag}'"
                            break
                        } else {
                            error "Error checking image version. HTTP Status: ${response}"
                        }
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the docker image from the dockerfile present in the current workspace
                    echo "Building Docker Image ${imageName}:v${imageTag}"
                    dockerImage = docker.build("${imageName}:v${imageTag}")
                    if (dockerImage == null) {
                        error("Docker image '${imageName}:v${imageTag}' creation failed.")
                    } else {
                        echo "Docker Image '${imageName}:${imageTag}' created successfully."\
                    }
                    
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Push the docker to DockerHub
                    echo "Pushing Docker Image on DockerHub"
                    docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                        dockerImage.push()
                    }
                    echo "Docker Images pushed successfully."
                }
            }
        }
        stage('Deploy Application') {
            steps {
                script {
                    // Run Docker container
                    bat "docker run --name WeatherApp.V${imageTag} -d ${imageName}:v${imageTag}"
                    sleep(time: 30, unit: 'SECONDS') // Sleep for 2 minute
                }
            }
        }
        stage('Stop Docker Conatiner') {
            steps {
                script {
                    // Stop and remove container after the job completes
                    bat "docker stop WeatherApp.V${imageTag}"
                    bat "docker rm WeatherApp.V${imageTag}"
                }
            }
        }
    }
}