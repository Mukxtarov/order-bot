class Helper(object):
    def __init__(self):
        super(Helper, self).__init__()

    @staticmethod
    def isChannel(message):
        if not message.post:
            return True
        elif not message.to_id.channel_id:
            return True
        else:
            return False
