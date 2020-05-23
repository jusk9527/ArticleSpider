
# 使用cookie

class CookiesMiddleWare(object):

    def process_request(self, request, spider):
        cookies = request.meta.get('cookies')
        if cookies:
            request.cookies = cookies
