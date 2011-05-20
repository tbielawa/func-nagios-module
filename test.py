#!/usr/bin/env python
# Some basic tests against the func-nagios module.

import func.overlord.client as fc



if __name__ == '__main__':
    n = fc.Client('griddle')

    n.nagios.schedule_svc_downtime('lnx.cx', services=['HTTP'], minutes=5)
    n.schedule_host_downtime('tbielawa.com', minutes=5)

    n.schedule_hostgroup_host_downtime('int-servers', minutes=5)
    n.schedule_hostgroup_svc_downtime('ext-servers', minutes=5)

    n.schedule_servicegroup_host_downtime('ircservers', minutes=5)
    n.schedule_servicegroup_svc_downtime('httpservers', minutes=5)

    n.disable_host_svc_notifications('redstonefoundries.com')
    n.enable_host_svc_notifications('redstonefoundries.com')

    n.disable_host_notifications('peopleareducks.com')
    n.enable_host_notifications('peopleareducks.com')

    n.disable_svc_notifications('redstonefoundries.com', services=['Minecraft'])
    n.enable_svc_notifications('redstonefoundries.com', services=['Minecraft'])

    n.disable_servicegroup_host_notifications('httpservers')
    n.enable_servicegroup_host_notifications('httpservers')

    n.disable_servicegroup_svc_notifications('ircservers')
    n.enable_servicegroup_svc_notifications('ircservers')

    n.disable_hostgroup_host_notifications('int-servers')
    n.enable_hostgroup_host_notifications('int-servers')

    n.disable_hostgroup_svc_notifications('linux-servers')
    n.enable_hostgroup_svc_notifications('linux-servers')
