
def sendSuccessEmail(price) {
    emailext body: "\nFinalizado com sucesso \nBuild finazalido ${BUILD_NUMBER}\n",
        mimeType: 'text/html',
        subject: "<span>[Jenkins] Build Finalizado</span>",
        to: "fabcovalesci@gmail.com"
}

def sendBuildFailureEmail(price) {
    emailext body: "\n<p>Finalizado com sucesso \nBuild finazalido ${BUILD_NUMBER}\n",
        mimeType: 'text/html',
        subject: "<span>[Jenkins] Build Failure</span>",
        to: "fabcovalesci@gmail.com"
}


// TZ=America/Sao_Paulo

// H/2 * * * *

pipeline {
    
    agent any
    environment {
        URL_API_AWS = credentials('URL_API_AWS')
    }

    stages {
        stage('Git clone projeto') {
            steps {
                git branch: 'main',
                url: 'https://github.com/fabriciocovalesci/web_scraping_loterias'
            }
        }
        stage('Build image') {
            steps {
                script {
                    sh "echo ${URL_API_AWS}"
                    echo "Building image docker ..."
                    sh "docker build -t loteria_bot ."   
                }        
              } 
            }
        stage('Run container') {
            steps {
                script {
                    echo "Running image docker ..."
                    sh "docker run --rm  loteria_bot -u ${URL_API_AWS}" 
                }
            }
        }
    }
    post {
        always {
            echo 'Finalizando pipeline'
            // deleteDir()
        }
        success {
            echo 'Finalizado com sucesso'
            // sendSuccessEmail()
        }
         failure {
            echo 'Falhou :('
            // sendBuildFailureEmail()
        }
    }
}
