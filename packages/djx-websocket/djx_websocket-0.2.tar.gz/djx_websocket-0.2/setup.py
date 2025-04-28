# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djx_websocket',
 'djx_websocket.migrations',
 'djx_websocket.serializers',
 'djx_websocket.views']

package_data = \
{'': ['*'],
 'djx_websocket': ['.git/*',
                   '.git/hooks/*',
                   '.git/info/*',
                   '.git/logs/*',
                   '.git/logs/refs/heads/*',
                   '.git/logs/refs/remotes/origin/*',
                   '.git/objects/pack/*',
                   '.git/refs/heads/*',
                   '.git/refs/remotes/origin/*']}

install_requires = \
['channels-redis>=4.1.0,<5.0.0',
 'channels>=4.0.0,<5.0.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'uvicorn[standard]>=0.24.0.post1,<0.25.0']

setup_kwargs = {
    'name': 'djx-websocket',
    'version': '0.2',
    'description': '',
    'long_description': '',
    'author': 'nope',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
