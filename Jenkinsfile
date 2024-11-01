pipeline {
    agent any
    environment {
        // Python Binary Path
        python = '"C:\\Program Files\\Python313\\python.exe"'
        python_version = '3.13.0' 
        unitTestcaseList = "unittestcase.txt"
        //PYTHONPATH = '"C:\\Users\\lalit\\Desktop\\projects\\weather"'
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
        stage('Validate Python') {
            steps {
                script {
                    // Checking python version
                    echo "Valiadting Python Version..."

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
        stage('Launch Application') {
            steps {
                script {
                    // Launch GUI (Tkinter) application
                    echo 'Launching Weather Application (background process)...'

                    def status = bat(script: "start ${python} app\\main.py", returnStatus: true)

                    if (status == 0) {
                        echo ("Weather application launched successfully.")
                    } else{
                        echo ("Failed to launch weather application")
                    }
                }
            }
        }
        stage('Unit Tests') {
            steps {
                script {
                    // Reading Unit Testcase File
                    def testCases = readFile(unitTestcaseList).trim().split('\n')
                    for (testCase in testCases) {
                        def status = bat(script: "${python} -m unittest test.${testCase}", returnStatus: true)
                        if ($status != 0) { 
                            error "Unit testcases '${testcase}' failed."
                        }
                    }
                }
            }
        }
        stage('Integration Tests') {
            steps {
                script {
                    stage ('unit') {
                        bat "${python} -m unittest test.test_main"
                    }
                    stage ('integration') {
                        bat "${python} -m unittest test.test_main"
                    }
                    // Run Unit Testcases
                    //echo 'Running Unit Testcases for main.py'
                    //bat "${python} -m unittest test.test_integration"
                }
            }
        }
        stage('Build Docker Image') {
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
                            echo "Next Image version should be ${imageName}:v${imageTag}"
                            break
                        } else {
                            echo "Error checking image version. HTTP Status: ${response}"
                        }
                    }

                    sleep(time: 2, unit: 'SECONDS') // Sleep for 2 seconds

                    // Build the docker image from the dockerfile present in the current workspace
                    echo "Building Docker Image ${imageName}:v${imageTag}"
                    dockerImage = docker.build("${imageName}:v${imageTag}")
                    echo "Docker Image ${imageName}:${imageTag} built successfully."

                    sleep(time: 2, unit: 'SECONDS') // Sleep for 2 seconds

                    // Push the docker to DockerHub
                    echo "Pushing Docker Image on DockerHub"
                    docker.withRegistry('https://index.docker.io/v1/', 'Notepad') {
                        dockerImage.push()
                    }
                    echo "Docker Images pushed successfully."
                    sleep(time: 2, unit: 'SECONDS') // Sleep for 2 minute

                    // Remove the docker image from the local environment after pushing
                    //echo "Removing Docker Image"
                    //bat "docker rmi ${imageName}:v${imageTag}"
                    //echo "Docker Image removed successfully."
                }
            }
        }
        stage('Run Docker Container') {
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