pipeline {
    options {
        timestamps()
    }
    agent { label 'server2' }
    environment { 
     PROJECT_DIR = '/mobeq'
     SSH_USER = "ght"
     SSH_HOST =  "177.71.116.28"
    }
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
            when {
                not {
                    tag "${env.TAG_NAME}"
                }
            }
            steps {
                
                sh 'dockerd-entrypoint.sh &'
                sh 'sleep 10 && export DOCKER_BUILDKIT=1 && docker compose -f scripts/docker-compose-test.yml up --build --exit-code-from app'
                archiveArtifacts artifacts: 'steve_logs.log', fingerprint: true
            }
            
        }
        stage('Push to Production') {
            when {
                tag "${env.TAG_NAME}"
            }
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'juca-ci', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "echo 'This is a sample text file' > xablau"
                    '''
                    sh '''
                        rsync -Pav -e "ssh -i $SSH_KEY" ./ ${SSH_USER}@${SSH_HOST}:~/steve-certi-deploy
                    '''
                    sh '''
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "docker compose up"
                    '''
                }
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
