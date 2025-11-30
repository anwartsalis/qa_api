pipeline {
    agent any

    tools {
        allure 'allure-manual'
    }

    stages {
        stage('Run Tests in Docker') {
            steps {
                script {
                    docker.image('python:3.13.9-slim').inside("--network jenkins-network") {
                        stage('Install Dependencies') {
                            sh '''
                                cd /var/jenkins_home/workspace/SQA_Code_Along
                                ls -la
                                pip install -r requirements.txt
                            '''
                        }
                        
                        stage('Run Tests') {
                            sh '''
                                cd /var/jenkins_home/workspace/SQA_Code_Along
                                pytest test_api.py -v --alluredir=allure-results
                            '''
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            // allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            allure includeProperties: false, jdk: '', properties: [[key: 'allure.report.name', value: 'Judul Custom Laporan Saya'], [key: 'allure.report.title', value: 'Test Execution Report']], resultPolicy: 'LEAVE_AS_IS', results: [[path: 'allure-results']]
        }
    }
}