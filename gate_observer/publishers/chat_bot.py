import logging
import requests

LOG = logging.getLogger(__file__)

class ChatBotClient(object):
    """Sends jenkins event information to the chat bot server"""

    def __init__(self, config):
        self.domain = config.get('domain')
        self.meeting_id = config.get('meeting_id')
        self.port = config.get('port')
        self.session = requests.Session()
        self.session.auth = ('%s@%s' % (config.get('user'), self.domain),
                             config.get('password'))

    def post(self, url, data):
        try:
           resp = self.session.post(url, data=data)
           if resp.status_code == 401:
               raise requests.RequestException('(401) Unauthorized')
           resp.raise_for_status()
        except requests.RequestException as e:
            LOG.error('error during post: %s', e)
            raise

    def execute(self, data):
        url = ('http://%(domain)s:%(port)s/push/meeting:%(meeting_id)s'
               % {'domain': self.domain,
                  'port': self.port,
                  'meeting_id': self.meeting_id})
        self.post(url, data)
        LOG.info("Message '%s' successfully sent to '%s'",
                 data, url)
