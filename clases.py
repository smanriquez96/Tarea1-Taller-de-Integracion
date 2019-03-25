from octopus import Octopus

# this Octopus instance we'll run 4 threads,
# automatically start listening to the queue and
# we'll in-memory cache responses for 10 seconds.
otto = Octopus(
    concurrency=10, auto_start=True, cache=True,request_timeout_in_seconds = 10,
    expiration_in_seconds=20)

def handle_url_response(url, response):
    print("hola")
    # do something with response

otto.enqueue('http://www.google.com', handle_url_response)
otto.enqueue('http://www.facebook.com', handle_url_response)
otto.enqueue('http://www.yahoo.com', handle_url_response)

# this request will come from the cache
otto.enqueue('http://www.google.com', handle_url_response)

otto.wait()  # waits until queue is empty or timeout is ellapsed
