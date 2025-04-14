pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -e .'  
            }
        }
        stage('Test') {
            steps {
                sh 'python -m unittest discover -s tests -p "test_*.py"'
            }

            }
        }
    

}