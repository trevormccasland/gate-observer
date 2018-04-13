import testtools

import mock
import requests

from gate_observer.publishers import chat_bot
from gate_observer.publishers import exceptions as exc


class ChatBotClientTestCase(testtools.TestCase):

    def setUp(self):
        super(ChatBotClientTestCase, self).setUp()
        self.config = {'domain': 'chatbots.com',
                       'port': 123456,
                       'user': 'jenkins_chatbot',
                       'password': 'secret',
                       'meeting_id': '1234567890'}
        patch = mock.patch('requests.Session')
        self.session = patch.start().return_value
        self.addCleanup(patch.stop)
        self.client = chat_bot.ChatBotClient(self.config)
        self.assertEqual(('%s@%s' % (self.config.get('user'),
                                     self.config.get('domain')),
                          self.config.get('password')),
                         self.session.auth)

    def test_post(self):
        url = 'test url'
        data = 'test data'
        self.session.post.return_value = mock.Mock(status_code=200)
        self.client.post(url, data)
        self.session.post.assert_called_once_with(url, data=data)

    def test_post_unauthorized(self):
        url = 'test url'
        data = 'test data'
        self.session.post.return_value = mock.Mock(status_code=401)
        self.assertRaises(exc.UnAuthorizedRequest, self.client.post, url, data)
        self.session.post.assert_called_once_with(url, data=data)

    def test_post_failure(self):
        url = 'test url'
        data = 'test data'
        self.session.post.side_effect = [requests.RequestException]
        self.assertRaises(exc.PostFailure, self.client.post, url, data)
        self.session.post.assert_called_once_with(url, data=data)

    def test_execute(self):
        data = 'test data'
        url = ('http://%(domain)s:%(port)s/push/meeting:%(meeting_id)s'
               % {'domain': self.client.domain,
                  'port': self.client.port,
                  'meeting_id': self.client.meeting_id})
        with mock.patch.object(self.client, 'post') as mock_post:
            self.client.execute(data)
            mock_post.assert_called_once_with(url, data)
