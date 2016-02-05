# sshkey-manager
Linux与OS X系统下ssh命令行配置脚本 v0.0.1<br>
我造的又一个轮子。。。<br>
因为感觉手动编辑文件去配置ssh的主机设置很麻烦，所以写了这个小脚本，用于交互式配置。<br>
目前只支持<br>
* Host
* HostName
* User
* IdentityFile

这几项配置，后续会增加更多。同时，我正在翻译OpenSSH的客户端配置文档，有兴趣的朋友可以近期关注该项目的网站。<br>
对于不支持的参数，key-manager不会做任何改动，会原封不动地再次写回硬盘。<br>

####使用方法：
目前支持四种操作：
* install
* init
* add
* delete

支持的参数有
* -h
* -v

install：用于初次安装。使用`./km.py install`（前提是，你要给它可执行权限）自动在/usr/local/bin下创建软链，以后就能直接使用
`km ...`了<br>
init：在系统上建立~/.ssh/config配置，写入一个#字符。如果你已经有了个人配置，不要使用该参数。<br>
add：添加操作。交互式。<br>
delete：删除操作，交互式。<br>

涉及到写配置的操作，由于都调用rebuild()函数来重新写回硬盘，在该函数中预先做了备份工作。如果由于该脚本导致ssh不能工作，只需要将.ssh目录下的config.bak替换掉config即可。

-h：输出帮助信息，退出程序<br>
-v：输出版本，退出程序<br>
