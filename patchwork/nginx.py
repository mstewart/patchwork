
import packages
from fabric.api import put, sudo
from StringIO import StringIO

def proxy(site_name, site_root, proxied_url='http://localhost:3000'):
    """
    Proxy to a backend webserver on ``proxied_url``,
    but serving some static files via nginx from the ``site_root``.

    Todo: Add support for site_root=None to just proxy.
    Todo: Test on non-fedora-like systems.
    """
    packages.install(['nginx'])
    nginx_site_conf = """
server {
    # forward user's IP address to backend server
    proxy_set_header  X-Real-IP  $remote_addr;

    proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;

    listen 80;
    server_name %(site_name)s;

    root   %(site_root)s;
    try_files $uri @proxied_appserver;

    location @proxied_appserver {
        proxy_pass %(proxied_url)s;
    }
}
""" % locals()
    put(StringIO(nginx_site_conf),
            '/etc/nginx/conf.d/%(site_name)s.conf' % locals(),
            use_sudo=True)
    sudo('service nginx start && service nginx reload')
