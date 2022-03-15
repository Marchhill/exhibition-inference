from django.http import HttpResponseBadRequest
import subprocess


class FilterHostMiddleware:
    # https://stackoverflow.com/a/36222755/7254995
    # https://docs.djangoproject.com/en/4.0/topics/http/middleware/#writing-your-own-middleware

    def __init__(self, get_response):
        self.get_response = get_response
        # Boilerplate; One-time configuration and initialization.

    def __call__(self, request):
        ALLOWED_HOSTS = subprocess.run(["hostname", "-I"], capture_output=True)\
            .stdout.decode().strip().split(' ') + ["127.0.0.1"]
        if request.META.get("HTTP_HOST") in ALLOWED_HOSTS:
            # Allow (hostname -I) and 127.0.0.1 only
            # (hostname -I) is dynamically evaluated during runtime, so website
            # still works (at the new IP address) if its site-local IP changes
            # midway. Without this middleware, website will always be served on
            # whatever the IP address is at install/deploy-time.
            return self.get_response(request)
        return HttpResponseBadRequest()

        # httpHost = request.META.get("HTTP_HOST")
        # if httpHost == "127.0.0.1":
        #     # always allow localhost: needed to POST readings to database
        #     return self.get_response(request)

        # httpHostPacked = IPv4Address(httpHost).packed
        # httpHost24SubnetPrefixStr = f"{httpHostPacked[0]}.{httpHostPacked[1]}.{httpHostPacked[2]}"

        # localIPs = subprocess.run(["hostname", "-I"], capture_output=True)\
        #     .stdout.decode().strip().split(' ')
        # for ip in localIPs:
        #     packed = IPv4Address(ip).packed
        #     if packed[0] == 127:
        #         continue  # skip all loopback IP addresses
        #     if f"{packed[0]}.{packed[1]}.{packed[2]}" == httpHost24SubnetPrefixStr:
        #         # allow all IPs from same /24 subnet
        #         return self.get_response(request)
        # return HttpResponseBadRequest()
