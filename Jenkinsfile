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
        }
        stage('Deliver') {
            agent {
                docker {
                    image 'cdrx/pyinstaller-linux:python2'
                }
            }
            steps {
                sh 'pyinstaller --onefile sources/library.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/library'
                }
            }
        }
        stage('Email'){
            steps{
                always{
                    mail to:"pawarakshada13@gmail.com", subject:"Status of pipeline: ${currentBuild.fullDisplayName}", 
                   // body: "Library Management System Application keeps the track of the books present in the library. \n ${env.BUILD_URL} has result ${currentBuild.result}."
                    body: """<html>
<body>
<style>
table{
    border: 1px solid black;
    border-collapse: collapse;
    background-color: #D3FCFB;
}

th, td {
    border: 1px solid black;
    padding: 5px;
    text-align: left;
    }
    
th, td#t01{
    border: 1px solid black;
    padding: 5px;
    text-align: left;
    background-color: #2890C8;
    }
    
    
</style>
<h3><b><i>Library Management System Test Build Summary</i></b></h3>
<table style="width:100%">
  <tr>
    <td id="t01"><b>Job Status</b></td>
    <td id="t01">Success</td>
  </tr>
  <tr>
    <td><b>Project</b></td>
    <td>Project1</td>
  </tr>
  <tr>
    <td><b>Environment</b></td>
    <td>Test</td>
  </tr>
   <tr>
    <td><b>Docker Image Version</b></td>
    <td>imagename:${env.BUILD_NUMBER}</td>
  </tr>
  <tr>
    <td><b>BUILD Logs</b></td>
    <td>${env.BUILD_URL}</td>
  </tr>
  </table>"""
            //recipientProviders: [[$class: 'DevelopersRecipientProvider']]
        }
        }
    }
    }
}