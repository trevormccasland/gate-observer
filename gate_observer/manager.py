import Queue
import sys
import time

from gate_observer.gate import observer

class JenkinsManager(object):
    """Reads data from Queue and notifies the publisher"""

    def __init__(self, server, jobs):
        # the all encompassing queue
        self.q = Queue.Queue()
        # for managing threads
        self.workers = []
        # for filtering
        self.jobs = jobs
        # for sharing host info to the observers
        self.server = server
        for job in self.jobs:
            worker = observer.JobObserver('%s-thread' % job,
                                          self.server, job, self.q)
            self.workers.append(worker)

    def start(self):
        for worker in self.workers:
            worker.start()
        try:
            while True:
                time.sleep(100)
        except (SystemExit, KeyboardInterrupt):
            print('keyboard interrupt.. manager exiting')
            self.stop()

    def stop(self):
        for worker in self.workers:
            if worker.is_alive():
                try:
                    worker.stop()
                except Exception as e:
                    print('Something happened while stopping %s, err: %s',
                          (worker.name, e))
        sys.exit(1)
