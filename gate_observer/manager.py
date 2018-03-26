import logging
import Queue
import time

from gate_observer import observer

LOG = logging.getLogger(__file__)


class JenkinsManager(object):
    """Reads data from Queue and notifies the publisher"""

    def __init__(self, server, jobs, publishers):
        # the all encompassing queue
        self.q = Queue.Queue()
        # for filtering
        self.jobs = jobs
        # for communicating
        self.publishers = publishers
        # for sharing host info to the observers
        self.server = server
        # for managing threads
        self.workers = []
        for job in self.jobs:
            worker = observer.JobObserver('%s-thread' % job,
                                          self.server, job, self.q)
            self.workers.append(worker)

    def publish(self, data):
        for publisher in self.publishers:
            publisher.execute(data)

    def _process_queue(self):
        while True:
            try:
                data = self.q.get_nowait()
                self.publish(data)
            except Queue.Empty:
                time.sleep(0.1)
            except Exception as err:
                LOG.info('Something happened while publishing data: %s', err)

    def start(self):
        for worker in self.workers:
            worker.start()
        try:
            self._process_queue()
        except (SystemExit, KeyboardInterrupt):
            LOG.info('keyboard interrupt.. manager exiting')
        finally:
            self.stop()

    def stop(self):
        for worker in self.workers:
            if worker.is_alive():
                try:
                    worker.stop()
                except Exception as e:
                    LOG.info('Something happened while stopping %s, err: %s',
                             (worker.name, e))
