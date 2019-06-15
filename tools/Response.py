class Response(object):

    STATUS_OK = "ok"
    STATUS_FAIL = "fail"

    def __init__(self, status, error, data):
        self.status = status
        self.error = error
        self.data = data

    def get(self):
        return {
            "status": self.status,
            "error": self.error,
            "data": self.data
        }