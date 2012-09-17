#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
MacPacbot

Copyright (c) 2010 Dexter.Yy
Released under GPL Licenses.
"""

import sys, os, re
import yaml
from mako.template import Template
import subprocess as sub
from optparse import OptionParser
import pickle


class Pacbot():
    """auto proxy configuration toolkit
    """
    networkInfo = {}
    template = """function FindProxyForURL(url, host) {
    %for server in data:
        ${server['name']} = "${server['type'] + (' ' + server['ip'] if server['ip'] else '')}";
        %for site in server['rules']:
            %if site['type'] == 'shell':
                if ( shExpMatch(url, '${site['rule']}') ) return ${server['name']};
            %elif site['type'] == 'regexp':
                if ( new RegExp("${site['rule']}").test(url) ) return ${server['name']};
            %else:
                if ( new RegExp("${site['rule']}", "i").test(url) ) return ${server['name']};
            %endif
        %endfor
    %endfor
    return default_config;
}
    """

    def __init__(self):
        self.servers = {}
        self.addServer('default_config', type='direct')

    def enable(self, pacfile):
        """enable PAC file"""
        service = self.networkInfo['service']
        url = 'file://localhost' + pacfile
        for cmd in [
                ['networksetup', '-setautoproxystate', service, 'off'],
                ['networksetup', '-setautoproxyurl', service, url],
                ['networksetup', '-setautoproxystate', service, 'on']
            ]:
            sub.check_call(cmd)

    def disable(self):
        """disable PAC"""
        sub.check_call(['networksetup', '-setautoproxystate', self.networkInfo['service'], 'off'])

    def getCode(self):
        """get code of PAC script"""
        tpl = Template(self.template)
        data = self.servers.values()
        return tpl.render(data=data)

    def save(self, pacfile):
        """save PAC script"""
        open(pacfile, 'w').write(self.getCode())

    def updateNetworkInfo(self, **data):
        if not data:
            for networkservice in sub.Popen(['networksetup', '-listallnetworkservices'],
                                     stdout=sub.PIPE).stdout:
                networkservice = re.sub(b'\n', b'', networkservice).strip()
                info = sub.Popen(['networksetup', '-getInfo', networkservice],
                          stdout=sub.PIPE).stdout.read()
                if re.search(b'IP\s+address:\s*\d', info):
                    self.networkInfo["service"] = networkservice
                    break
        else:
            self.networkInfo.update(data)
        return self.networkInfo

    def addServer(self, servername, type='DIRECT', proxy=None, rules=[]):
        """add proxy server"""
        type = type.upper()
        if type == 'HTTP':
            type = 'PROXY'
        rulelist = []
        for rule in rules:
            rerule = re.search(r'/(.+)/', rule)
            if rerule:
                rulelist.append({
                    'rule': rerule.group(1),
                    'type': 'regexp'
                })
            else:
                isShell = re.search(r'\*', rule)
                rulelist.append({
                    'rule': rule,
                    'type': 'shell' if isShell else 'domain'
                })
        self.servers[servername] = {
            'name': servername,
            'ip': proxy,
            'type': type,
            'rules': rulelist
        }


def main(argv=None):
    if argv is None:
        argv = sys.argv

    opt = OptionParser()
    opt.add_option("-s", "--state",
                   dest="state",
                   help="setautoproxystate(on/off)",
                   type="string")
    opt.add_option("-u", "--update",
                   dest="update",
                   help="update NetworkInfo",
                   action="store_true")
    opt.add_option("-o", "--output",
                   dest="outputfile",
                   help="write output to <file>",
                   metavar="FILE")
    (opt, args) = opt.parse_args()

    isEnable = opt.state != 'off'

    BIN_PATH = os.path.dirname(__file__)

    if len(args) > 0:
        configfile = args[0]
    else:
        configfile = os.path.join(BIN_PATH, 'rules.ypac')

    if not os.path.isfile(configfile):
        print('Sorry, I need rules file')
        return

    CONFIG_PATH = os.path.dirname(os.path.abspath(configfile))

    outputfile = opt.outputfile or os.path.join(CONFIG_PATH, 'rules.pac')

    cachefile = os.path.join('/tmp/networkInfoCache.pkl')

    pacbot = Pacbot()

    def update_cache():
        networkInfo = pacbot.updateNetworkInfo()
        cache = open(cachefile, 'wb')
        pickle.dump(networkInfo, cache)

    if not opt.update and os.path.isfile(cachefile):
        try:
            cache = open(cachefile, 'r')
            networkInfo = pickle.load(cache)
            pacbot.updateNetworkInfo(**networkInfo)
        except:
            update_cache()
    else:
        update_cache()

    if opt.update:
        if isEnable:
            pacbot.enable(outputfile)
        else:
            pacbot.disable()
        return

    if isEnable:
        data = yaml.load(open(configfile, 'r'))
        for k, v in data.items():
            pacbot.addServer(k, **v)
        pacbot.save(outputfile)
        pacbot.enable(outputfile)
    else:
        pacbot.disable()


if __name__ == "__main__":
    exit = main()
    if exit:
        sys.exit(exit)
