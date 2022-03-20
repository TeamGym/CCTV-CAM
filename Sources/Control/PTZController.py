class PTZController:
    def __init__(self, context):
        self.__host = context.tapoHost
        self.__user = context.tapoUser
        self.__password = context.tapoPassword
