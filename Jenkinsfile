pipeline {
    agent any
    environment {
        // Global Variables
        python = '"C:\\Program Files\\Python313\\python.exe"'
        python_version = '3.13.0' 
        unitTestcaseList = "unittestcase.txt"
        integrationTestcaseList = "integrationtestcase.txt" 
        def imageName = 'lalitbits2023/weather'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone GIT repository
                echo 'Cloning Repository...'
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
            }
        }
        stage('Check Python Version') {
            steps {
                script {
                    // Check python version 
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
                    // Run unit testcase
                    echo 'Running Unit Testcases...'

                    // Reading unit testcase file
                    def testCases = readFile(unitTestcaseList).trim().split('\n')

                    for (testCase in testCases) {
                        echo "Running Testcase : ${testCase}"
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
                    // Run integration testcase
                    echo 'Running Integration Testcases...'

                    // Reading integration testcase File
                    def testCases = readFile(integrationTestcaseList).trim().split('\n')

                    for (testCase in testCases) {
                        echo "Running Testcase : ${testCase}"
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
                    // Check docker deamon and find next docker image 
                    echo "Preparing Build Environment..."

                    // Run a Docker command and capture the exit status
                    def status = bat(script: "docker --version", returnStatus: true)

                    // Check if the Docker daemon is running
                    if (status == 0) {
                        echo "Docker daemon is up and running."
                    } else {
                        error "Docker daemon is not running. Please start Docker and try again."
                    }

                    // Check docker image on Docker Hub
                    imageTag = 1
                    while (true) {
                        def response = bat (
                            script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/v${imageTag}",
                            returnStdout: true
                        ).trim()

                        response = response.split()[-1]

                        if (response == "200") {
                            echo "Image '${imageName}:v${imageTag}' exists on Docker Hub."
                            imageTag += 1
                        } else if (response == "404") {
                            echo "Next Image '${imageName}:v${imageTag}'"
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
                    // Build the docker image 
                    echo "Building Docker Image..."
                    dockerImage = docker.build("${imageName}:v${imageTag}")
                    if (dockerImage == null) {
                        error("Docker image '${imageName}:v${imageTag}' creation failed.")
                    } else {
                        echo "Docker image '${imageName}:v${imageTag}' build successfully."\
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Push the docker image to DockerHub
                    echo "Pushing Docker Image..."
                    docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                        dockerImage.push()
                    }
                    def response = bat (
                            script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/v${imageTag}",
                            returnStdout: true
                    ).trim()
                    response = response.split()[-1]
                    if (response == "200") {
                        echo "Docker Images '${imageName}:${imageTag}' pushed successfully on DockerHub."
                    } else {
                        error "Failed to push docker image '${imageName}:${imageTag}' on DockerHeb."
                    }
                    bat "docker rmi ${imageName}:v${imageTag}"
                }
            }
        }
        stage('Deploy Application') {
            steps {
                script {
                    // Pull Docker Image from DockerHub
                    echo "Pulling Docker Image..."
                    def status = bat(script: "docker pull ${imageName}:v${imageTag}", returnStatus: true)
                    if (status == 0) {
                        echo "Docker Image '${imageName}:v${imageTag}' pulled successfully."
                    } else {
                        error "Failed to pull Docker Image '${imageName}:v${imageTag}'"
                    }
                    // Run Docker Container
                    echo "Deploying application..."
                    status = bat(script: "docker run --name WeatherApp.V${imageTag} -d ${imageName}:v${imageTag}", returnStatus: true)
                    if (status == 0) {
                        echo "Application deployed successfully in TEST environment."
                    } else {
                        error "Application failed to deploy in TEST environment."
                    }
                }
            }
        }
        //stage('Stop Docker Conatiner') {
            //steps {
                //script {
                    // Stop and remove container after the job completes
                    //bat "docker stop WeatherApp.V${imageTag}"
                    //bat "docker rm WeatherApp.V${imageTag}"
                //}
            //}
        //}
    }
}