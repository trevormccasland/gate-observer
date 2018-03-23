import logging
import time

import jenkins

from gate_observer.gate import client
from gate_observer import manager

LOG_FILE_NAME = 'gate-observer.log'
JENKINS_INFO = ('http://localhost:8080',
                'admin',
                '661055624b7643dda09f05085867c2cc')
JOB_NAMES = ['test-job', 'test-job2']

def main():
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG)
    server = jenkins.Jenkins(*JENKINS_INFO)
    jenkins_manager = manager.JenkinsManager(server, JOB_NAMES)
    try:
        jenkins_manager.start()
    except (KeyboardInterrupt, SystemExit):
        print('Keyboard interrupt.. main exiting')
        jenkins_manager.stop()

if __name__ == "__main__":
    main()
