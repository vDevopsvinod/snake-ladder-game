pipeline {
    agent { label 'built-in' }

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
                    sh '/opt/sonar-scanner/bin/sonar-scanner ' +
                       '-Dsonar.projectKey=snake-ladder-game ' +
                       '-Dsonar.sources=src ' +
                       '-Dsonar.tests=tests'
                }
                echo "✅ SonarQube analysis completed"
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
                echo "✅ Quality Gate PASSED"
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    docker.build("snake-ladder-game:${BUILD_ID}")
                }
                echo "✅ Docker built"
            }
        }

        stage('Tests') {
            steps {
                sh "docker run --rm snake-ladder-game:${BUILD_ID} sh -c 'pip install pytest && python3 -m pytest tests/ -v'"
                echo "✅ Tests passed"
            }
        }
    }

    post {
        success { echo "🎉 Build #${BUILD_NUMBER} SUCCESS" }
        failure { echo "❌ Build #${BUILD_NUMBER} FAILED" }
    }
}
