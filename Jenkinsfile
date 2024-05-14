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
                    image 'docker:dind-rootless'
                    args '--privileged -u root:root'
                }
            }
            steps {
                sh 'dockerd-entrypoint.sh &'
                sh 'sleep 10 && export DOCKER_BUILDKIT=1 && docker compose -f scripts/docker-compose-test.yml up --build --exit-code-from app'
                sh "cp steve_logs.log ${WORKSPACE}"
                archiveArtifacts artifacts: 'steve_logs.log', fingerprint: true
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
