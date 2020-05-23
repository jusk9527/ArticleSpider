from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import random
import time

# 重试的中间件，解决一些代理啊！异常重试的一些解决方法，根据业务需要，更改重试
class CustomRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):

        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 如果返回了[500, 502, 503, 504, 522, 524, 408]这些code，换个proxy试试
            proxy = random.choice()
            request.meta['proxy'] = proxy
            return self._retry(request, reason, spider) or response

        return response

    # RetryMiddleware类里有个常量，记录了连接超时那些异常
    # EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
    #                       ConnectionRefusedError, ConnectionDone, ConnectError,
    #                       ConnectionLost, TCPTimedOutError, ResponseFailed,
    #                       IOError, TunnelError)
    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            # 这里可以写出现异常那些你的处理
            proxy = random.choice()
            request.meta['proxy'] = proxy
            time.sleep(random.randint(3, 5))
            return self._retry(request, exception, spider)
    # _retry是RetryMiddleware中的一个私有方法，主要作用是
    # 1.对request.meta中的retry_time进行+1
    # 2.将retry_times和max_retry_time进行比较，如果前者小于等于后者，利用copy方法在原来的request上复制一个新request，并更新其retry_times，并将dont_filter设为True来防止因url重复而被过滤。
    # 3.记录重试reason