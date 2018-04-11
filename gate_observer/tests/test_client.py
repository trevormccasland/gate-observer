import testtools

import jenkins
import mock

from gate_observer import client


class JenkinsClientTestCase(testtools.TestCase):

    def setUp(self):
        super(JenkinsClientTestCase, self).setUp()
        self.server = mock.Mock()
        self.client = client.JenkinsClient(self.server)
        self.job = 'test job'
        self.build = 1234

    def test_is_build_building(self):
        build_info = {'building': True}
        self.server.get_build_info.return_value = build_info
        result = self.client.is_build_building(self.job, self.build)
        self.server.get_build_info.assert_called_once_with(self.job,
                                                           self.build)
        self.assertEqual(build_info['building'], result)

    def test_is_build_building_exception(self):
        self.server.get_build_info.side_effect = [jenkins.NotFoundException]
        result = self.client.is_build_building(self.job, self.build)
        self.server.get_build_info.assert_called_once_with(self.job,
                                                           self.build)
        self.assertEqual(False, result)
