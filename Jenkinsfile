pipeline {
    agent none
    stages {
        stage('Start'){
            steps{
                // Send build started notifications
                sendNotificatins 'STARTED'
            }
        }
        stage('Build') {
            agent {
                docker {
                    image 'python:3-alpine'
                }
            }
            steps {
                sh 'python -m py_compile sources/library.py'
                stash(name: 'compiled-results', includes: 'sources/*.py*')
            }
            post{
                success{
                    mail to:"pawarakshada13@gmail.com", subject:"SUCCESS ${currentBuild.fullDisplayName}", body: "We passed all test cases."
                    // Archive the built artifacts
                    archive includes:'pkg/*.gem'
                }
                failure{
                    mail to:"pawarakshada13@gmail.com", subject:"FAILURE ${currentBuild.fullDisplayName}", body: "We failed test cases."
                }
            }
        }
        stage('Test') { 
            agent {
                docker {
                    image 'qnib/pytest' 
                }
            }
            steps {
                sh 'py.test --junit-xml test-reports/results.xml sources/library_test.py' 
            }
            post{
                success{
                    mail to:"pawarakshada13@gmail.com", subject:"SUCCESS ${currentBuild.fullDisplayName}", body: "We passed all test cases."
                    // Publish html
                    publishHTML target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'coverage',
                        reportFiles: 'index.html',
                        reportName: 'RCov Report'
                    ]
                }
                failure{
                    mail to:"pawarakshada13@gmail.com", subject:"FAILURE ${currentBuild.fullDisplayName}", body: "We failed test cases."
                }
            }
            post {
                always {
                    //junit 'test-reports/results.xml'
                    sendNotificatins currentBuild.result 
                }
            }
        }
    }
}