import six


class PublisherException(Exception):
    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        super(PublisherException, self).__init__(self.message % kwargs)
        self.msg = self.message % kwargs

    if six.PY2:
        def __unicode__(self):
            return unicode(self.msg)

    def __str__(self):
        return self.msg


class PostFailure(PublisherException):
    message = "An error occured sending '%(data)s' to %(url)s"


class UnAuthorizedRequest(PublisherException):
    message = ("The requested url '%(url)s' denied the user %(user)s"
               "with the password '%(password)s")
