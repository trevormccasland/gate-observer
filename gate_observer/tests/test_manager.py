import testttools

import mock

from gate_observer import manager

class JenkinsManagerTestCase(testtools.TestCase):

    def setUp(self):
        super(JenkinsManagerTestCase, self).setUp()
        self.server = mock.Mock()
        self.jobs = ['test-job', 'test-job2']
        self.publishers =[mock.Mock()]
        patch = mock.patch('gate_observer.gate.observer.JobObserver')
        mock_observer = patch.start()
        self.addCleanUp(patch.stop)
        self.manager = manager.JenkinsMananger(self.server,
                                               self.jobs,
                                               self.publishers)
        self.assertEqual(len(self.jobs), len(self.manager.workers))

    def test_publish(self):
        self.manager.publish('foo')
        for publisher in self.publishers:
            publisher.execute.assert_called_once_with('foo')
