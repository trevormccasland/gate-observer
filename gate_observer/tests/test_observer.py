import testtools

import mock

from gate_observer import observer

BUILD_NUMBER = 1234


class JobObserverTestCase(testtools.TestCase):

    def setUp(self):
        super(JobObserverTestCase, self).setUp()
        self.queue = mock.Mock()
        self.server = mock.Mock()
        self.job = 'test job'
        patch = mock.patch('gate_observer.client.JenkinsClient')
        self.mock_client = patch.start()
        self.addCleanup(patch.stop)
        mock_obj = self.mock_client.return_value
        mock_obj.get_current_build_number.return_value = BUILD_NUMBER
        mock_obj.is_build_building.side_effect = [True, True, False]
        self.observer = observer.JobObserver('test observer', self.server,
                                             self.job, self.queue)
        self.start_message = ('build %s for job %s started' %
                              (BUILD_NUMBER, self.job))
        self.stop_message = ('build %s for job %s stopped' %
                             (BUILD_NUMBER, self.job))

    def test_run(self):
        self.assertRaises(StopIteration, self.observer.run)
        calls = [mock.call(self.start_message), mock.call(self.stop_message)]
        self.queue.put.assert_has_calls(calls)
