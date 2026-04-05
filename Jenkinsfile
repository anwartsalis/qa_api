pipeline {
    agent any

    tools {
        allure 'allure'
    }

    environment {
        TELEGRAM_BOT_TOKEN = '7293069411:AAHmtG7oQfJbFFABuXgWJIStTRcDqBSaX0w'
        TELEGRAM_CHAT_ID = '-4112006641'
    }

    stages {
        stage('Run Tests in Docker') {
            steps {
                script {
                    docker.image('python:3.13.9-slim').inside("--network jenkins-network") {
                        stage('Install Dependencies') {
                            sh '''
                                cd /var/jenkins_home/workspace/pengecekan_api
                                ls -la
                                pip install -r requirements.txt
                            '''
                        }
                        
                        stage('Run Tests') {
                            sh '''
                                cd /var/jenkins_home/workspace/pengecekan_api
                                pytest test_api.py -v --alluredir=allure-results
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Generate Report & Kirim Telegram') {
            steps {
                script {
                    // Generate Allure Report
                    allure includeProperties: false, 
                           jdk: '', 
                           properties: [
                               [key: 'allure.report.name', value: 'Report nih'], 
                               [key: 'allure.report.title', value: 'Test Execution Report']
                           ], 
                           resultPolicy: 'LEAVE_AS_IS', 
                           results: [[path: 'allure-results']]
                    
                    // Prepare notif
                    def allureReportUrl = "${env.BUILD_URL}allure/"
                    def status = currentBuild.result ?: 'SUCCESS'
                    
                    // test summary
                    def summary = ''
                    try {
                        if (fileExists('allure-report/widgets/summary.json')) {
                            def summaryJson = readJSON file: 'allure-report/widgets/summary.json'
                            summary = """
Test Summary:
Total: ${summaryJson.statistic.total}
Passed: ${summaryJson.statistic.passed}
Failed: ${summaryJson.statistic.failed}
Broken: ${summaryJson.statistic.broken}
Skipped: ${summaryJson.statistic.skipped}

"""
                        }
                    } catch (Exception e) {
                        echo "Could not read summary: ${e.message}"
                        summary = ""
                    }
                    
                    // Bikin pesen chat
                    def message = """
Test Automation Report

Automation yang enih:  ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: ${status}
Duration: ${currentBuild.durationString}
Date: ${new Date().format('dd-MM-yyyy HH:mm')}

${summary}Allure Report: ${allureReportUrl}
Jenkins Build: ${env.BUILD_URL}
                    """.replaceAll("'", "'\\\\''")
                    
                    // Kirim Telegram
                    sh """
                    curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage \
                    -d chat_id=${TELEGRAM_CHAT_ID} \
                    -d disable_web_page_preview=false \
                    -d text='${message}'
                    """
                }
            }
        }
    }
    
    post {
        failure {
            node('') {
                script {
                    def message = """
Build Failed

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}

Console: ${env.BUILD_URL}console
                    """.replaceAll("'", "'\\\\''")
                    
                    sh """
                    curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage \
                    -d chat_id=${TELEGRAM_CHAT_ID} \
                    -d text='${message}'
                    """
                }
            }
        }
    }
}
