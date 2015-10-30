from contextlib import closing
import pytest
import six

import urllib

import requests

from flex.http import (
    normalize_response, _tornado_available
)


#
#  Test normalizatin of the response object from the requests library
#
def test_response_normalization(httpbin):
    raw_response = requests.get(httpbin.url + '/get')

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == 200


#
#  Test normalization of urllib response object
#
def test_urllib_response_normalization(httpbin):
    if six.PY2:
        raw_response = urllib.urlopen(httpbin.url + '/get')
    else:
        raw_response = urllib.request.urlopen(httpbin.url + '/get')

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == 200


#
#  Test normalization of urllib2 response object
#
@pytest.mark.skipif(six.PY3, reason="No urllib2 in python3")
def test_urllib2_response_normalization(httpbin):
    import urllib2
    raw_response = urllib2.urlopen(httpbin.url + '/get')

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == 200


#
# Test tornado response object
#
@pytest.mark.skipif(not _tornado_available, reason="tornado not installed")
def test_tornado_response_normalization(httpbin):
    import tornado.httpclient

    with closing(tornado.httpclient.HTTPClient()) as client:
        raw_response = client.fetch(
            httpbin.url + '/get',
            headers={'Content-Type': 'application/json'}
        )

    response = normalize_response(raw_response)

    assert response.path == '/get'
    assert response.content_type == 'application/json'
    assert response.url == httpbin.url + '/get'
    assert response.status_code == 200
