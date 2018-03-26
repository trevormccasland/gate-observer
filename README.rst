Install
=======

sudo -E pip install -r requirements.txt && sudo python setup.py install


Usage
=====

gate-observer


Proxy
-----
This project uses the requests module you can set these by setting
the environment variables ``HTTP_PROXY`` and ``HTTPS_PROXY``.

::

    $ export HTTP_PROXY="http://10.10.1.10:3128"
    $ export HTTPS_PROXY="http://10.10.1.10:1080"

    $ python
    >>> import requests
    >>> requests.get('http://example.org')

http://docs.python-requests.org/en/master/user/advanced/#proxies


Config
======

gate-observer.conf
------------------

[default]
log_file_name=etc/gate-observer.log
log_level=10

[jenkins]
host=localhost
port=8080
user=admin
password=admin
job_names=test-job
          test-job2
          test-job3


publishers.conf
---------------

This assumes some server is listening to illustrate a chat bot example

[chat_bot]
domain=chatbots.com
port=123456
user=jenkins_chatbot
password=<password>
meeting_id=<chatroom_meeting_id>


Test Environment
================

1. Use a jenkins container from https://github.com/jenkinsci/docker
2. create jobs and put those names in your jenkins config section.
3. start the program, start a build and you should see logging similar to:
  INFO:/usr/local/lib/python2.7/dist-packages/gate_observer/publishers/chat_bot.pyc:Message 'build 9 for job test-job2 started' successfully sent to <interpolated uri>
  INFO:/usr/local/lib/python2.7/dist-packages/gate_observer/observer.pyc:(test-job2-thread) build 9 for job test-job2 stopped
  DEBUG:urllib3.connectionpool:<proxy> "POST <interpolated uri> HTTP/1.1" 200 None
