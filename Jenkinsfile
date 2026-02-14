pipeline {
    agent any

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
            echo "🎉 Build #${BUILD_NUMBER} succeeded!"
        }
        failure {
            echo "❌ Build #${BUILD_NUMBER} failed!"
        }
    }
}
