#!/usr/bin/env groovy

import java.util.Date

def isMaster = env.BRANCH_NAME == 'master'
def isStaging = env.BRANCH_NAME == 'staging'
def start = new Date()
def err = null
def dockerImageName = 'oseme-techguy/python-pdf-annotation-api-demo'


String jobInfoShort = "${env.JOB_NAME} ${env.BUILD_DISPLAY_NAME}"
String jobInfo = "${env.JOB_NAME} ${env.BUILD_DISPLAY_NAME} \n${env.BUILD_URL}"
String buildStatus
String timeSpent

currentBuild.result = "SUCCESS"

try {
    node {
        deleteDir()
        // Pull code
        checkout scm
        /* Requires the Docker Pipeline plugin to be installed */
        // docker.image('python:3.7-alpine').inside("-u 0") {
        //     withEnv(['LC_ALL=C.UTF-8', 'LANG=C.UTF-8']) {
        //         stage('Prepare Environment') {
        //             sh 'apk add --update --no-cache python3 git gcc make musl-dev'
        //             sh 'pip3 install pipenv'
        //             sh 'pipenv install --deploy --system'
        //             sh 'pipenv install --dev pylint'
        //         }
        //         stage('Code Quality') {
        //             sh 'pipenv run lint'
        //         }
        //     }
        // }
        stage('Code Quality') {
            // sh 'pipenv run lint'
            echo "Skipping code quality check"
        }
        // Run Docker builds and push to Dockerhub on Staging and Master branches alone
        if (isStaging || isMaster) {
            if(isStaging) {
                dockerImageName = dockerImageName + ':' + 'staging';
            }
            else{
                dockerImageName = dockerImageName + ':' + 'latest';
            }
            stage('Build') {
                // Delete previous image(s) and ignore if there is an error
                sh 'docker rmi '+ dockerImageName + ' || true'
                // Build docker image
                sh 'docker build -t ' + dockerImageName + ' .'
                // Push built image
                sh 'docker push ' + dockerImageName
                // Delete image locally after push
                sh 'docker rmi '+ dockerImageName + ' || true'
            }
        }
    }
} catch (caughtError) {
    err = caughtError
    currentBuild.result = "FAILURE"
} finally {
    timeSpent = "\nTime spent: ${timeDiff(start)}"

    if (err) {
        slackSend (color: 'danger', message: "Build failed: ${jobInfo} ${timeSpent}")
        throw err
    } else {
        if (currentBuild.previousBuild == null) {
            buildStatus = 'Build: first time'
        } else if (currentBuild.previousBuild.result == 'SUCCESS') {
            buildStatus = 'Build: complete'
        } else {
            buildStatus = 'Build: initialized'
        }

        slackSend (color: 'good', message: "${buildStatus}: ${jobInfo} ${timeSpent}")
        if (isStaging || isMaster) {
            slackSend (color: 'good', message: "*${env.BRANCH_NAME}* branch deployed to Dockerhub")
        }
    }
}


def timeDiff(st) {
    def delta = (new Date()).getTime() - st.getTime()
    def seconds = delta.intdiv(1000) % 60
    def minutes = delta.intdiv(60 * 1000) % 60

    return "${minutes} min ${seconds} sec"
}