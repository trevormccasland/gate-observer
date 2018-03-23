import jenkins
import logging
import threading
import time

from gate_observer.gate import client

LOG = logging.getLogger(__file__)

class JobObserver(threading.Thread):
    """puts events onto a shared q given a jenkins server and job name"""

    def __init__(self, name, server, job, q):
        super(JobObserver, self).__init__(name=name)
        self.q = q
        self.job = job
        self.server = server
        self.client = client.JenkinsClient(self.server)
        self.build_number = self.client.get_current_build_number(job)
        self.exit = False

    def is_building(self):
        return self.client.is_build_building(self.job, self.build_number)

    def _wait_for_build_to_stop(self):
         while True:
             # wait for the build to stop
             if not self.is_building():
                 print('build %s for job %s '
                       'stopped' % (self.build_number, self.job))
                 break

    def run(self):
        while True:
            self.build_number = self.client.get_current_build_number(self.job)
            if self.exit:
                print('thread exiting..')
                break
            if self.is_building():
                print('build %s for job %s '
                      'started' % (self.build_number, self.job))
                self._wait_for_build_to_stop()
            print('build %s for job %s is running: '
                  '%s' % (self.build_number, self.job, self.is_building()))

    def stop(self):
        self.exit = True
