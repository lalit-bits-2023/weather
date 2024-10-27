pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                echo 'clone....'
                git branch: 'main', url: 'https://github.com/lalit-bits-2023/weather.git'
            }
        }

    }

    #post {
    #    failure {
    #        script {
    #            // Email notification on failure
    #            mail to: '2022MT93720@wilp.bits-pilani.ac.in',
    #                 subject: "Jenkins Job Failed: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
    #                 body: "Build #${env.BUILD_NUMBER} of Jenkins job '${env.JOB_NAME}' has failed.\nCheck console output at ${env.BUILD_URL} for details."
    #        }
    #    }
    #    always {
    #        cleanWs() // Clean up workspace
    #    }
    #}
    
}
