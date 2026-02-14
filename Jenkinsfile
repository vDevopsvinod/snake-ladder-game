cd ~/snake-ladder-game

cat > Jenkinsfile << 'EOF'
pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "snake-ladder-game"
        IMAGE_TAG = "${BUILD_ID}"
        GITHUB_REPO = "https://github.com/vDevopsvinod/snake-ladder-game.git"
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
                    // Build Docker image with build args
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}", 
                        "--build-arg BUILD_ID=${BUILD_ID} " +
                        "--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') " +
                        "--build-arg VCS_REF=${GIT_COMMIT} " +
                        "."
                    )
                }
                echo "✅ Docker image built: ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Run unit tests inside container
                    sh """
                        docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} \\
                            sh -c "pip install pytest && python3 -m pytest tests/ -v"
                    """
                }
                echo "✅ All tests passed!"
            }
        }
        
        stage('Trivy Scan') {
            steps {
                script {
                    // Install Trivy if not present (will do in Phase 5)
                    sh """
                        if ! command -v trivy &> /dev/null; then
                            echo "⚠️ Trivy not installed (will configure in Phase 5)"
                        else
                            trivy image --severity CRITICAL,HIGH --no-progress ${IMAGE_NAME}:${IMAGE_TAG} || true
                        fi
                    """
                }
                echo "✅ Security scan completed (detailed scan in Phase 5)"
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                script {
                    // Save Docker image as artifact
                    sh "docker save ${IMAGE_NAME}:${IMAGE_TAG} -o ${IMAGE_NAME}-${IMAGE_TAG}.tar"
                    archiveArtifacts artifacts: "${IMAGE_NAME}-${IMAGE_TAG}.tar", fingerprint: true
                }
                echo "✅ Docker image archived: ${IMAGE_NAME}-${IMAGE_TAG}.tar"
            }
        }
    }
    
    post {
        always {
            // Cleanup Docker images to save space
            sh """
                docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                docker image prune -f
            """
        }
        success {
            echo "🎉 Pipeline completed successfully! Build #${BUILD_NUMBER}"
        }
        failure {
            echo "❌ Pipeline failed! Build #${BUILD_NUMBER}"
            // Could add Slack/email notification here
        }
    }
}
EOF

# Commit to GitHub
git add Jenkinsfile
git commit -m "feat: add Jenkinsfile for CI/CD pipeline"
git push origin main
