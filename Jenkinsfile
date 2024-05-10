pipeline {
    options {
        timestamps()
    }
    agent { label 'server2' }
    environment { PROJECT_DIR = '/mobeq' }
    stages {
        stage('Prepare enviroment') {
            stages {
                stage('Update and Init Submodules') {
                    steps {
                        sh 'git submodule update --init --recursive'
                    }
                }
            }
        }
        stage('Agent test') {
            agent {
                docker {
                    reuseNode true
                    image 'docker:dind'
                    args '-u root:sudo -v ${WORKSPACE}:/mobeq -w /mobeq -e TERM=xterm'
                }
            }
            steps {
                sh 'docker-compose -f scripts/docker-compose-test.yml up --build --exit-code-from app'
            }
        }
    }
    post {
        // Clean after build
        always {
            cleanWs()
	}
    }
}
