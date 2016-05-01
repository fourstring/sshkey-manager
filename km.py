#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import sysconfig
import textwrap

platform = sysconfig.get_platform()
if platform[0:5] == 'linux':
    user = os.popen('whoami').read().replace('\n', '')
    if user == 'root':
        prefix = '/'
    else:
        prefix = '/home'
elif platform[0:6] == 'macosx':
    prefix = '/Users'
else:
    print('Don\' support platfrom!')
    exit(-1)
path = '%s' % (prefix + '/' + os.popen('whoami').read().replace('\n', ''))

class Host:
    def __init__(self, host):
        self.host = host
        self.identity = None
        self.port = 22
        self.unsupported = {}


def init():
    try:
        os.mkdir(path + '/.ssh', 0o700)
    except FileExistsError:
        pass
    os.popen("echo '#' > %s/.ssh/config" % (path))
    print('Init Finshed')


def host_build(file=path + '/.ssh/config'):
    hosts = []
    config_file = open(file, 'r')
    for line in config_file:
        if line[0] == '#':
            continue
        elif line.strip() == '':
            continue
        key, value = line.strip().split(' ')
        if key == 'Host':
            hosts.append(Host(value))
        elif key == 'HostName':
            hosts[len(hosts) - 1].hostname = value
        elif key == 'User':
            hosts[len(hosts) - 1].user = value
        elif key == 'IdentityFile':
            hosts[len(hosts) - 1].identity = value
        elif key == 'Port':
            hosts[len(hosts) - 1].port = value
        else:
            hosts[len(hosts) - 1].unsupported[key] == value
    return hosts


def add(hosts, host, hostname, user, identityfile=None, port=22):
    hosts.append(Host(host))
    hosts[len(hosts) - 1].hostname = hostname
    hosts[len(hosts) - 1].user = user
    hosts[len(hosts) - 1].identity = identityfile
    hosts[len(hosts) - 1].port = port


def delete(hosts, host):
    for i in range(0, len(hosts)):
        if hosts[i].host == host:
            del hosts[i]
            return


def rebuild(hosts):
    os.popen('cp %s %s' % (path + '/.ssh/config', path + '/.ssh/config.bak'))
    config_file = open(path + '/.ssh/config', 'w')
    for host in hosts:
        template = '''
Host {host}
HostName {hostname}
User {user}
IdentityFile {identity}
Port {port}

            '''
        config_file.write(
                textwrap.dedent(
                        template.format(host=host.host, hostname=host.hostname, user=host.user,
                                        identity=host.identity,
                                        port=host.port)))
        for key in sorted(host.unsupported):
            config_file.write('%s %s' % (key, host.unsupported(key)))


def install():
    try:
        cwd = os.getcwd()
        os.popen('rm /usr/local/bin/km')
        os.popen('ln -s %s/km.py /usr/local/bin/km' % (cwd))
        os.popen('chmod +x /usr/local/bin/km')
    except PermissionError:
        print('Install Failed.Please use as root!')
        exit(-1)


if __name__ == '__main__':
    if '-v' in sys.argv:
        print('ssh-key-manager v0.0.3 programmed by fourstring https://n4l.pw')
    elif '-h' in sys.argv:
        helpmsg = '''
SSH Key-manager A software to manage your ssh hosts config
Usage:km [action]

Actions:
install -- install the software in your system(use './km.py install')
init -- initialize the ssh personal configuration on your system(if you have had your config,don't use the action)
add -- add a host
delete -- delete a host
'''
        print(helpmsg)
    elif 'add' in sys.argv:
        hosts = host_build()
        while True:
            host = input('Please input host ID:')
            hostname = input('Please input host\'s address:')
            user = input('Please input host\'s user:')
            identityfile = input('Please input host\'s private key (use Absolute path,but support ~):')
            port = input('Please input host\'s port(default is 22):') if input(
                    'Please input host\'s port(default is 22):') else 22
            add(hosts, host, hostname, user, identityfile, port)
            while True:
                opinion = input('Do you want to add more hosts?[y/n]')
                if opinion == 'y':
                    break
                elif opinion == 'n':
                    rebuild(hosts)
                    print(
                            'Your configuration has been writed to ~/.ssh/config,if there is any exception,program has backuped the primary config file as config.bak')
                    exit(0)
                else:
                    print('Please input y or n!')
                    continue
    elif 'delete' in sys.argv:
        while True:
            hosts = host_build()
            host = input('Please input host ID:')
            delete(hosts, host)
            while True:
                opinion = input('Do you want to delete more hosts?[y/n]')
                if opinion == 'y':
                    break
                elif opinion == 'n':
                    rebuild(hosts)
                    print(
                            'Your configuration has been writed to ~/.ssh/config,if there is any exception,program has backuped the primary config file as config.bak')
                    exit(0)
                else:
                    print('Please input y or n!')
                    continue
    elif 'install' in sys.argv:
        install()
        exit(0)
    elif 'init' in sys.argv:
        init()
        exit(0)
    else:
        helpmsg = '''
SSH Key-manager A software to manage your ssh hosts config
Usage:km [action]

Actions:
install -- install the software in your system(use './km.py install')
init -- initialize the ssh personal configuration on your system(if you have had your config,don't use the action)
add -- add a host
delete -- delete a host
'''
        print(helpmsg)
