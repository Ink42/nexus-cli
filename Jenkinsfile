pipeline {
    agent any
    stages {
        stage('Setup') {
            agent 
                docker {
                    image 'python:3.14-rc-slim'
                
                }
            }
            steps {
                sh'python3 -v'
                sh'python -v'
            }
        }

    
}