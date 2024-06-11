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
                        rsync -Pav -e "ssh -i $SSH_KEY" ./ ${SSH_USER}@${SSH_HOST}:~/steve-certi-deploy
                    '''
                   sh '''
                        deployment_footer="CERTI Build:$TAG_NAME"
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "echo $deployment_footer > ~/steve-certi-deploy/src/main/resources/webapp/static/text/certi-version.txt"
                    '''

                    sh '''
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "docker compose -f ~/steve-certi-deploy/docker-compose-production.yml down"
                    '''
                    sh '''
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "docker compose -f ~/steve-certi-deploy/docker-compose-production.yml up -d --build"
                    '''
                    sh '''
                        ./scripts/wait-for.sh --host=${SSH_HOST} --port=8180 --timeout=240 
                    '''
                }
            }
            post {
                success {
                    withCredentials([string(credentialsId: 'jenkins-google-chat-hook', variable: 'WEBHOOK')]) {
                            sh '''
                            curl --request POST \
                            --url "$WEBHOOK" \
                            --header 'Content-Type: application/json' \
                            --data "{
                                'text': 'Status pipeline: *Steve Certi foi atualizado!* \n Servidor: http://${SSH_HOST} \n Documentação: http://${SSH_HOST}/docs \n _Bitbucket_: ${GIT_URL} \n _Branch_: ${BRANCH_NAME} \n _Commit_: ${GIT_COMMIT} \n Jenkins Job: ${BUILD_URL}'
                            }"
                            '''
                    }
                }
                failure {
                    withCredentials([string(credentialsId: 'jenkins-google-chat-hook', variable: 'WEBHOOK')]) {
                            sh '''
                            curl --request POST \
                            --url "$WEBHOOK" \
                            --header 'Content-Type: application/json' \
                            --data "{
                                'text': 'Status pipeline: *Deploy Steve Certi falhou!* \n _Bitbucket_: ${GIT_URL} \n _Branch_: ${BRANCH_NAME} \n _Commit_: ${GIT_COMMIT}  \n Jenkins Job: ${BUILD_URL}'
                            }"
                            '''
                    }
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
