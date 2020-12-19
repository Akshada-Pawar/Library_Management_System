pipeline {
    agent none
    stages {
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
                always{
                    mail to:"pawarakshada13@gmail.com", subject:"Status of pipeline: ${currentBuild.fullDisplayName}", 
                    body: "Library Management System Application keeps the track of the books present in the library. ${env.BUILD_URL} has result ${currentBuild.result}."
                    
                }
            }
        }
    }
}