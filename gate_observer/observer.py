import jenkins
import logging
import threading
import time

from gate_observer import client

LOG = logging.getLogger(__file__)


class JobObserver(threading.Thread):
    """puts events onto a shared queue given a jenkins server and job name"""

    def __init__(self, name, server, job, queue):
        super(JobObserver, self).__init__(name=name)
        self.exit = False
        self.queue = queue
        self.job = job
        self.server = server
        self.client = client.JenkinsClient(self.server)
        try:
            self.build_number = self.client.get_current_build_number(job)
        except jenkins.NotFoundException:
            LOG.error("(%s) Could not find job '%s'", self.name, self.job)
            raise SystemExit

    def is_building(self):
        return self.client.is_build_building(self.job, self.build_number)

    def _wait_for_build_to_stop(self):
        while self.is_building():
            # wait for the build to stop
            time.sleep(0.1)
        message = ('build %s for job %s stopped' %
                   (self.build_number, self.job))
        LOG.info('(%s) %s', self.name, message)
        self.queue.put(message)

    def run(self):
        while not self.exit:
            self.build_number = self.client.get_current_build_number(self.job)
            if self.is_building():
                message = ('build %s for job %s started' %
                           (self.build_number, self.job))
                LOG.info('(%s) %s', self.name, message)
                self.queue.put(message)
                self._wait_for_build_to_stop()
        LOG.info('(%s) thread exiting..', self.name)

    def stop(self):
        self.exit = True
