pipeline {
    agent { label 'built-in' }

    environment {
        IMAGE_NAME = "snake-ladder-game"
        IMAGE_TAG = "${BUILD_ID}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ Checked out commit: ${GIT_COMMIT}"
            }
        }

        stage('SonarQube Scan') {
            steps {
                script {
                    // withSonarQubeEnv automatically sets SONAR_HOST_URL and SONAR_TOKEN
                    withSonarQubeEnv('SonarQube-Server') {
                        sh """
                            docker run --rm \\
                              -e SONAR_HOST_URL='${SONAR_HOST_URL}' \\
                              -e SONAR_TOKEN='${SONAR_TOKEN}' \\
                              -v '${WORKSPACE}:/usr/src' \\
                              sonarsource/sonar-scanner-cli:4.8 \\
                              -Dsonar.projectKey=snake-ladder-game \\
                              -Dsonar.sources=src \\
                              -Dsonar.tests=tests \\
                              -Dsonar.projectBaseDir=/usr/src
                        """
                    }
                }
                echo "✅ SonarQube analysis completed"
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    def qg = waitForQualityGate()
                    if (qg.status != 'OK') {
                        error "❌ Quality Gate FAILED: ${qg.status}"
                    }
                }
                echo "✅ Quality Gate PASSED"
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
                echo "✅ Docker image built: ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} sh -c \\
                    "pip install pytest && python3 -m pytest tests/ -v"
                """
                echo "✅ All tests passed!"
            }
        }

        stage('Archive Artifacts') {
            steps {
                sh "docker save ${IMAGE_NAME}:${IMAGE_TAG} -o ${IMAGE_NAME}-${IMAGE_TAG}.tar"
                archiveArtifacts artifacts: "${IMAGE_NAME}-${IMAGE_TAG}.tar", fingerprint: true
                echo "✅ Docker image archived"
            }
        }
    }

    post {
        always {
            sh """
                docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                docker image prune -f || true
            """
        }
        success {
            echo "🎉 Build #${BUILD_NUMBER} succeeded with quality gate PASSED!"
        }
        failure {
            echo "❌ Build #${BUILD_NUMBER} failed!"
        }
    }
}
