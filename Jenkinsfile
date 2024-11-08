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
        stage('Parallel Stages - Build') {
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
        stage('Sanity Test') {
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
        stage('Parallel Stages - Test') {
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
        stage('Prepare Environments Setup') {
            steps {
                script {
                    // Check docker deamon and find next docker image 
                    echo "Preparing Environment Setup..."

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
        stage('Parallel Stages - Build Environments') {
            parallel {
                stage('Build DEV Environment') {
                    steps {
                        script {
                            // Build development enviromnment docker image 
                            echo "Creating Development Docker Image..."
                            dockerImage = docker.build("${imageName}:DEV.V${imageTag}", "-f dockerfile .")
                            if (dockerImage == null) {
                                error("Docker Image '${imageName}:DEV.V${imageTag}' creation failed.")
                            } else {
                                echo "Docker Image '${imageName}:DEV.V${imageTag}' created successfully."
                            }

                            // Push dev docker image to DockerHub
                            echo "Pushing Docker Image ${imageName}:DEV.V${imageTag} to docker registory..."
                            docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                                dockerImage.push()
                            }
                            def response = bat (
                                script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/DEV.V${imageTag}",
                                returnStdout: true
                            ).trim()
                            response = response.split()[-1]
                            if (response == "200") {
                                echo "Docker Images '${imageName}:DEV.V${imageTag}' pushed successfully on DockerHub."
                            } else {
                                error "Failed to push docker image '${imageName}:DEV.V${imageTag}' on DockerHeb."
                            }
                            bat "docker rmi ${imageName}:DEV.V${imageTag}"
                        }
                    }
                }
                stage('Build STG Environment') {
                    steps {
                        script {
                            // Build staging environment docker image 
                            echo "Creating Staging Docker Image..."
                            dockerImage = docker.build("${imageName}:STG.V${imageTag}", "-f dockerfile .")
                            if (dockerImage == null) {
                                error("Docker Image '${imageName}:STG.V${imageTag}' creation failed.")
                            } else {
                                echo "Docker Image '${imageName}:STG.V${imageTag}' created successfully."
                            }

                            // Push staging docker image to DockerHub
                            echo "Pushing Docker Image ${imageName}:STG.V${imageTag} to docker registory..."
                            docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                                dockerImage.push()
                            }
                            def response = bat (
                                script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/STG.V${imageTag}",
                                returnStdout: true
                            ).trim()
                            response = response.split()[-1]
                            if (response == "200") {
                                echo "Docker Images '${imageName}:STG.V${imageTag}' pushed successfully on DockerHub."
                            } else {
                                error "Failed to push docker image '${imageName}:STG.V${imageTag}' on DockerHeb."
                            }
                            bat "docker rmi ${imageName}:STG.V${imageTag}"
                        }
                    }
                }
                stage('Build PRD Environment') {
                    steps {
                        script {
                            // Build production environment docker image 
                            echo "Creating Production Docker Image..."
                            dockerImage = docker.build("${imageName}:PRD.V${imageTag}", "-f dockerfile .")
                            if (dockerImage == null) {
                                error("Docker Image '${imageName}:PRD.V${imageTag}' creation failed.")
                            } else {
                                echo "Docker Image '${imageName}:PRD.V${imageTag}' created successfully."
                            }

                            // Push prod docker image to DockerHub
                            echo "Pushing Docker Image ${imageName}:PRD.V${imageTag} to docker registory..."
                            docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                                dockerImage.push()
                            }
                            def response = bat (
                                script: "curl -s -o NUL -w %%{http_code} https://hub.docker.com/v2/repositories/%imageName%/tags/PRD.V${imageTag}",
                                returnStdout: true
                            ).trim()
                            response = response.split()[-1]
                            if (response == "200") {
                                echo "Docker Images '${imageName}:PRD.V${imageTag}' pushed successfully on DockerHub."
                            } else {
                                error "Failed to push docker image '${imageName}:PRD.V${imageTag}' on DockerHeb."
                            }
                            bat "docker rmi ${imageName}:PRD.V${imageTag}"
                        }
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