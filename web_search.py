import sys
import time
import urllib
import urllib.request
import random
import gzip
import re
from collections import Counter
import time

#	each query must have interval avoid drop by server
_interval_duckduckgo = 4
_last_time_duckduckgo = 0


# return query resp html string
def duckduckgo(keywords):
	global _interval_duckduckgo
	global _last_time_duckduckgo
	now = time.time()
	if now - _last_time_duckduckgo < _interval_duckduckgo:
		time.sleep( _interval_duckduckgo - (now - _last_time_duckduckgo))
	_last_time_duckduckgo = time.time()
	keywords = urllib.parse.quote(keywords)
	headers = {}
	headers['Accept-Encoding'] = 'gzip'#, deflate, br'
	headers['Accept-Language'] = 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3'
	headers['Cache-Control'] = 'no-cache'
	headers['connection'] = 'keep-alive'
	headers['Pragma'] = 'no-cache'
	headers['Upgrade-Insecure-Requests'] = '1'
	headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
	url = 'https://html.duckduckgo.com/html/?q=%s' % (keywords)
	print('url: %s' % (url), file=sys.stderr)
	html = ''
	try:
		req = urllib.request.Request(url, headers=headers)
		rsp = urllib.request.urlopen(req)
		byte_html = rsp.read()
		if rsp.getheader('content-encoding') == 'gzip':
			byte_html = gzip.decompress(byte_html)
		html = byte_html.decode("utf-8")
	except Exception as e:
		html = '%s (%s)' % (e, url)
		print(html, file=sys.stderr)
	return html

if __name__ == "__main__":
	print(sys.argv, file=sys.stderr)
	html = duckduckgo(sys.argv[1])
	print(html)
