pipeline {
    agent any
    environment {
        // Global Variables
        python = '"C:\\Program Files\\Python313\\python.exe"'
        python_version = '3.13.0' 
        unitTestcaseList = "unittestcase.txt"
        integrationTestcaseList = "integrationtestcase.txt" 
        imageName = 'lalitbits2023/weather'
    }
    stages {
        stage('Clone Repository') {
            steps {
                // Clone GIT repository
                echo 'Cloning Repository...'
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
            }
        }
        stage('Building') {
            parallel {
                stage('Validate Python Version') {
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
                stage('Install Python Dependencies') {
                    steps {
                        script {
                            // Install project dependencies using pip
                            echo 'Installing Dependencies...'

                            def status = bat(script: "${python} -m pip install -r requirements.txt", returnStatus: true)

                            if (status == 0) {
                                echo "Dependencies installed successfully."
                            } else {
                                error "Failed to install dependencies."
                            }
                        }
                    }
                }
            }
        }
        stage('Sanity Testing') {
            steps {
                script {
                    // Launch GUI (Tkinter) application
                    echo 'Launching Application in background...'
                    def status = 0
                    bat "start ${python} app\\main.py"
                    if (status != 0) {
                        echo ("Failed to start weather application")
                    }
                    else{
                        echo ("Weather application launched successfully.")
                    }
                }
            }
        }
        stage('U/I Testing') {
            parallel {
                stage('Unit Test') {
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
                stage('Integration Test') {
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
            }
        }
        stage('Preparing Env Setup') {
            steps {
                script {
                    // Check docker deamon and find next docker image 
                    echo "Preparing Environments Setup..."

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
                            script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/DEV.V${imageTag}",
                            returnStdout: true
                        ).trim()

                        response = response.split()[-1]

                        if (response == "200") {
                            echo "Image '${imageName}:DEV.V${imageTag}' exists on Docker Hub."
                            imageTag += 1
                        } else if (response == "404") {
                            echo "Next Image '${imageName}:DEV.V${imageTag}'"
                            break
                        } else {
                            error "Error checking image version. HTTP Status: ${response}"
                        }
                    }
                }
            }
        }
        stage('Building Environments') {
            parallel {
                stage('Building DEV Env') {
                    steps {
                        script {
                            // Build development enviromnment image 
                            echo "Creating Development Image..."
                            dockerImage = docker.build("${imageName}:DEV.V${imageTag}", "-f dockerfile .")
                            if (dockerImage == null) {
                                error("Docker Image '${imageName}:DEV.V${imageTag}' creation failed.")
                            } else {
                                echo "Docker Image '${imageName}:DEV.V${imageTag}' created successfully."
                            }

                            // Push the docker image to DockerHub
                            echo "Pushing Docker Image ${imageName}:DEV.V${imageTag} to DockerHub..."
                            docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                                dockerImage.push("DEV.V${imageTag}")
                            }
                            def response = bat (
                                script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/DEV.V${imageTag}",
                                returnStdout: true
                            ).trim()
                            response = response.split()[-1]
                            if (response == "200") {
                                echo "Docker Images '${imageName}:DEV.V${imageTag}' pushed successfully on DockerHub."
                            } else {
                                error "Failed to push docker image '${imageName}:DEV.V${imageTag}' on DockerHub."
                            }
                            bat "docker rmi ${imageName}:DEV.V${imageTag}"
                        }
                    }
                }
                stage('Building STG Env') {
                    steps {
                        script {
                            // Build staging environment image 
                            echo "Creating Staging Image..."
                            dockerImage = docker.build("${imageName}:STG.V${imageTag}", "-f dockerfile .")
                            if (dockerImage == null) {
                                error("Docker Image '${imageName}:STG.V${imageTag}' creation failed.")
                            } else {
                                echo "Docker Image '${imageName}:STG.V${imageTag}' created successfully."
                            }

                            // Push the docker image to DockerHub
                            echo "Pushing Docker Image ${imageName}:STG.V${imageTag} to DockerHub..."
                            docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                                dockerImage.push("STG.V${imageTag}")
                            }
                            def response = bat (
                                script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/STG.V${imageTag}",
                                returnStdout: true
                            ).trim()
                            response = response.split()[-1]
                            if (response == "200") {
                                echo "Docker Images '${imageName}:STG.V${imageTag}' pushed successfully on DockerHub."
                            } else {
                                error "Failed to push docker image '${imageName}:STG.V${imageTag}' on DockerHub."
                            }
                            bat "docker rmi ${imageName}:STG.V${imageTag}"
                        }
                    }
                }
                stage('Build PRD Env') {
                    steps {
                        script {
                            // Build production environment docker image 
                            echo "Creating Production Image..."
                            dockerImage = docker.build("${imageName}:PRD.V${imageTag}", "-f dockerfile .")
                            if (dockerImage == null) {
                                error("Docker Image '${imageName}:PRD.V${imageTag}' creation failed.")
                            } else {
                                echo "Docker Image '${imageName}:PRD.V${imageTag}' created successfully."
                            }

                            // Push the docker image to DockerHub
                            echo "Pushing Docker Image ${imageName}:PRD.V${imageTag} to DockerHub..."
                            docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                                dockerImage.push("PRD.V${imageTag}")
                            }
                            def response = bat (
                                script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/PRD.V${imageTag}",
                                returnStdout: true
                            ).trim()
                            response = response.split()[-1]
                            if (response == "200") {
                                echo "Docker Images '${imageName}:PRD.V${imageTag}' pushed successfully on DockerHub."
                            } else {
                                error "Failed to push docker image '${imageName}:PRD.V${imageTag}' on DockerHub."
                            }
                            bat "docker rmi ${imageName}:PRD.V${imageTag}"
                        }
                    }
                }
            }
        }
        stage('Deploy Development') {
            steps {
                script {
                    // Pull Docker Image from DockerHub
                    echo "Pulling Development Docker Image from DockerHub..."
                    def status = bat(script: "docker pull ${imageName}:DEV.V${imageTag}", returnStatus: true)
                    if (status == 0) {
                        echo "Docker Image '${imageName}:DEV.V${imageTag}' pulled successfully."
                    } else {
                        error "Failed to pull Docker Image '${imageName}:DEV.V${imageTag}'"
                    }
                    // Run Docker Container
                    echo "Deploying application in development environment..."
                    status = bat(script: "docker run --name WeatherApp.${imageTag} -d ${imageName}:DEV.V${imageTag}", returnStatus: true)
                    if (status == 0) {
                        echo "Application deployed successfully in DEV environment."
                    } else {
                        error "Application failed to deploy in DEV environment."
                    }
                }
            }
        }
        stage('Deploy Staging') {
            steps {
                script {
                    // Pull Docker Image from DockerHub
                    echo "Pulling Staging Docker Image from DockerHub..."
                    def status = bat(script: "docker pull ${imageName}:STG.V${imageTag}", returnStatus: true)
                    if (status == 0) {
                        echo "Docker Image '${imageName}:STG.V${imageTag}' pulled successfully."
                    } else {
                        error "Failed to pull Docker Image '${imageName}:STG.V${imageTag}'"
                    }
                    // Run Docker Container
                    echo "Deploying application in staging environment..."
                    status = bat(script: "docker run --name WeatherApp.${imageTag} -d ${imageName}:STG.V${imageTag}", returnStatus: true)
                    if (status == 0) {
                        echo "Application deployed successfully in STAGING environment."
                    } else {
                        error "Application failed to deploy in STAGING environment."
                    }
                }
            }
        }
    }
    post {
        success {
            emailext(
                subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "The job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' has completed successfully.",
                to: '2022MT93720@wilp.bits-pilani.ac.in'
            )
        }
        failure {
            emailext(
                subject: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "The job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' has failed. Please check the console output for details.",
                to: '2022MT93720@wilp.bits-pilani.ac.in'
            )
        }
    }
}