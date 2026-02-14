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
                echo "✅ SonarQube analysis completed"
            }
        }

        stage('Quality Gate') {
            steps {
                // SIMPLEST SYNTAX - no script block needed
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
                echo "✅ Quality Gate PASSED"
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
                echo "✅ Docker image built"
            }
        }

        stage('Run Tests') {
            steps {
                sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} sh -c 'pip install pytest && python3 -m pytest tests/ -v'"
                echo "✅ Tests passed"
            }
        }
    }

    post {
        success {
            echo "🎉 Build #${BUILD_NUMBER} SUCCESS"
        }
        failure {
            echo "❌ Build #${BUILD_NUMBER} FAILED"
        }
    }
}
