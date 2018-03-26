import jenkins


class JenkinsClient(object):
    """Just a wrapper around python-jenkins"""

    def __init__(self, server):
        self.server = server

    def get_current_build_number(self, job_name):
        return self.server.get_job_info(job_name)['nextBuildNumber'] - 1

    def is_build_building(self, job_name, build_number):
        try:
            info = self.server.get_build_info(job_name, build_number)
        except jenkins.NotFoundException:
            return False
        return info['building']
