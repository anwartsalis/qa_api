pipeline {
    agent any

    tools {
        allure 'allure-manual'
    }

    environment {
        TELEGRAM_BOT_TOKEN = credentials('1882130871:AAHZVRwcIFKlxdsId2buT0w_3wdaZzAEtpQ')
        TELEGRAM_CHAT_ID = '727162514'
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
            script {
                // Generate Allure Report
                allure includeProperties: false, 
                       jdk: '', 
                       properties: [
                           [key: 'allure.report.name', value: 'Laporan Saya'], 
                           [key: 'allure.report.title', value: 'Test Execution Report']
                       ], 
                       resultPolicy: 'LEAVE_AS_IS', 
                       results: [[path: 'allure-results']]
                
                // Prepare notification
                def allureReportUrl = "${env.BUILD_URL}allure/"
                def status = currentBuild.result ?: 'SUCCESS'
                
                // Get test summary
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
                
                // Build message
                def message = """
*Test Automation Report*

Project: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: ${status}
Duration: ${currentBuild.durationString}
Date: ${new Date().format('dd-MM-yyyy HH:mm')}

${summary}Allure Report: ${allureReportUrl}
Jenkins Build: ${env.BUILD_URL}
                """.replaceAll("'", "'\\\\''")
                
                // Send to Telegram
                sh """
                curl -s -X POST https://api.telegram.org/bot\${TELEGRAM_BOT_TOKEN}/sendMessage \
                -d chat_id=\${TELEGRAM_CHAT_ID} \
                -d parse_mode=Markdown \
                -d disable_web_page_preview=false \
                -d text='${message}'
                """
            }
        }
    }
}