# 这个可以自己设置个代理池，然后随机更换ip

class RandomProxyMiddleware(object):
    #动态设置ip代理
    # def process_request(self, request, spider):
    #     get_ip = GetIP()
    #     request.meta["proxy"] = get_ip.get_random_ip()

    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:1087"