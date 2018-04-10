import testtools

import mock

from gate_observer.publishers import exceptions as exc
from gate_observer import manager


class JenkinsManagerTestCase(testtools.TestCase):

    def setUp(self):
        super(JenkinsManagerTestCase, self).setUp()
        self.server = mock.Mock()
        self.jobs = ['test-job', 'test-job2']
        self.publishers = [mock.Mock()]
        patch = mock.patch('gate_observer.observer.JobObserver')
        self.mock_observer = patch.start()
        self.addCleanup(patch.stop)
        self.manager = manager.JenkinsManager(self.server,
                                              self.jobs,
                                              self.publishers)
        self.assertEqual(len(self.jobs), len(self.manager.workers))

    def test_start(self):
        test_data = 'foo'
        mock_queue = mock.Mock()
        mock_queue.get_nowait.side_effect = [test_data, exc.PublisherException]
        self.manager.queue = mock_queue
        self.manager.start()
        calls = [mock.call]
        self.assertEqual(len(self.jobs),
                         self.mock_observer.return_value.start.call_count)
        self.assertEqual(len(self.jobs),
                         self.mock_observer.return_value.stop.call_count)
        self.assertEqual(len(self.jobs),
                         self.mock_observer.return_value.is_alive.call_count)
        for publisher in self.publishers:
            publisher.execute.assert_called_once_with('foo')
