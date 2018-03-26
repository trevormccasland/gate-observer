import ConfigParser
import logging

import jenkins

from gate_observer import manager
from gate_observer.publishers import chat_bot


def get_publishers():
    config = ConfigParser.ConfigParser()
    config.read(['etc/publishers.conf'])
    return [
        chat_bot.ChatBotClient(dict(config.items('chat_bot')))
    ]
    

def main():
    config = ConfigParser.ConfigParser()
    config.read(['etc/gate-observer.conf'])
    logging.basicConfig(filename=config.get('default', 'log_file_name'),
                        level=config.getint('default', 'log_level'))
    host = ('http://%s:%s' % (config.get('jenkins', 'host'),
                              config.get('jenkins', 'port')))
    server = jenkins.Jenkins(host, config.get('jenkins', 'user'),
                             config.get('jenkins', 'password'))
    job_names = config.get('jenkins', 'job_names').splitlines()
    jenkins_manager = manager.JenkinsManager(server,
                                             job_names, get_publishers())
    try:
        jenkins_manager.start()
    except (KeyboardInterrupt, SystemExit):
        print('Keyboard interrupt.. main exiting')
        jenkins_manager.stop()

if __name__ == "__main__":
    main()
