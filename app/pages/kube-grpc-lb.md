# Load Balancing with Kube and GRPC

Suppose we have an intensive computation, such as a machine learning model,
running in a GRPC server in a Kube cluster. Usage has increased, and we want to
be able to horizonally scale our computations.

## Some Context

The language used is Python, and the GRPC server in question has a kube
`Service` object attached to it.


## What Doesn't Work

The simple solution is to increase the number of replicas of the GRPC server
instance that are running the model, say to 5 replicas. Then, we can use
GRPC's round robin load balancing to take advantage of these replicas

```
grpc.insecure_channel(url, (('grpc.lb_policy_name', 'round_robin'),))
```

After doing this, we can send many requests to the service, and we notice something
odd. One of the replicas recieves all the requests, and the other replicas
receive none.

This occurs because Kube services use L4 load balancing, running a proxy
in front of the service replicas. This is described at


https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies


GRPC meanwhile uses L7 load balancing, running at the application layer rather
than the routing layer. This means that the GRPC client will establish a connection
to a service replica, but then not recycle that connection. Therefore, all subsequent
requests will go to that replica. Thus preventing load balancing.

There is a good reason for this, creating TCP connections is expensive, so the
client reduces this cost by reusing connections. More detail on GRPC load balancing
can be found at


https://github.com/grpc/grpc/blob/master/doc/load-balancing.md


## What Does Work

We can achieve client side GRPC load balancing by using headless services. Headless
services in Kube do not have a kube proxy running in front of them. Rather,
when GRPC resolves the DNS name, it gets back a list of all available pods

<pre>
>>> list(dns.resolver.Resolver().query('<your pod ip address>'))

[DNS IN A rdata: 100.100.93.168, DNS IN A rdata: 100.125.108.148,
 DNS IN A rdata: 100.86.253.174, DNS IN A rdata: 100.86.63.214,
 DNS IN A rdata: 100.95.62.58]
</pre>

More details on headless services can be found at


https://kubernetes.io/docs/concepts/services-networking/#headless-services


GRPC supports client side load balancing, and so by setting the load balancing
policy to round robin as in the snippet above, it will automatically load
balance requests between replicas of the service.

At this point, load testing shows all of the replicas with an equal amount
of requests.

## Cautions

There are some things to watch out for when using headless services. First,
there are no port mappings, as these are done in the kube proxy. Second,
service replicas can restart with different cluster IP addresses. GRPC
thankfully handles this situation, but it may cause issues for other services.