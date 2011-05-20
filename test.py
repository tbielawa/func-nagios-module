#!/usr/bin/env python
# Some basic tests against the func-nagios module.

import func.overlord.client as fc

if __name__ == '__main__':
    NAGIOS_SERVER = 'griddle'
    n = fc.Client(NAGIOS_SERVER)

    # For testing it's best to roll through these in groups.

    ##############################################
    # DOWNTIME SCHEDULING TESTS
    ##############################################

    # These first three test downtime scheduling, but constrain the
    # operations to a single host at a time. This is to avoid
    # overlapping with the broader servicegroup and hostgroup downtime
    # commands. You can run these three tests together.

    # print n.nagios.schedule_svc_downtime('lnx.cx', ['HTTP','BIP IRC Proxy'], 2)
    # print n.nagios.schedule_svc_downtime('redstonefoundries.com', ['HTTP','Minecraft'], 2)
    # print n.nagios.schedule_host_downtime('tbielawa.com', 2)

    ##############################################
    # These next two commands also test downtime scheduling, but do so
    # to groups of servers. These can be ran together because one will
    # only set host-level downtime, while the other will set
    # service-level downtime.

    # print n.nagios.schedule_hostgroup_host_downtime('ext-servers', 2)
    # print n.nagios.schedule_hostgroup_svc_downtime('int-servers', 2)

    ##############################################
    # These next two tests can be ran together also for similar
    # reasons. The first command will set host-level down time for
    # each server in the 'ircservers' servicegroup. The second
    # command will set put the HTTP check into downtime for each host
    # in the 'httpservers' servicegroup.

    # print n.nagios.schedule_servicegroup_host_downtime('ircservers', 2)
    # print n.nagios.schedule_servicegroup_svc_downtime('httpservers', 2)

    ##############################################
    # NOTIFICATION TOGGLING TESTS
    ##############################################

    # These next sets of tests need to be run one at a time. They
    # aren't on a timer though, so cycling through them is only
    # limited by the time it takes you to perform verification. Run
    # the 'disable' command, verify the nagios event log or the target
    # host/service, then run the 'enable' command and check again.

    # If you have non-overlapping service/hostgroups you can run some
    # of these tests in parallel.

    # Disable all service notifications on redstonefoundries.com
    # print n.nagios.disable_host_svc_notifications('redstonefoundries.com')
    # Reenable all service notifications.
    # print n.nagios.enable_host_svc_notifications('redstonefoundries.com')

    ##############################################
    # Disable notifications for the peopleareducks.com host
    # print n.nagios.disable_host_notifications('peopleareducks.com')
    # Reenable notifications for peopleareducks.com
    # print n.nagios.enable_host_notifications('peopleareducks.com')

    ##############################################
    # Disable notifications for the Minecraft and HTTP services on
    # redstonefoundries.com
    # print n.nagios.disable_svc_notifications('redstonefoundries.com', ['Minecraft','HTTP'])
    # Reenable notifications for those services
    # print n.nagios.enable_svc_notifications('redstonefoundries.com', ['Minecraft', 'HTTP'])

    ##############################################
    # Disable host-level notifications for all hosts in the
    # 'httpservers' servicegroup
    # print n.nagios.disable_servicegroup_host_notifications('httpservers')
    # Reenable the host-level notifications
    # print n.nagios.enable_servicegroup_host_notifications('httpservers')

    ##############################################
    # Disable service notifications on every host in the 'ircservers'
    # servicegroup. The effect is limited to the particular service
    # associated with the given servicegroup.
    # print n.nagios.disable_servicegroup_svc_notifications('ircservers')
    # Reenable that service on every member of the 'ircservers' servicegroup
    # print n.nagios.enable_servicegroup_svc_notifications('ircservers')

    ##############################################
    # Disable host-level notifications on member of the 'int-servers' hostgroup
    # print n.nagios.disable_hostgroup_host_notifications('int-servers')
    # Reenable host-level notifications for every member host
    # print n.nagios.enable_hostgroup_host_notifications('int-servers')

    ##############################################
    # Disable ALL service notifications for every member of the
    # 'linux-servers' hostgroup
    # print n.nagios.disable_hostgroup_svc_notifications('linux-servers')
    # Reenable ALL service notifications for every member host
    # print n.nagios.enable_hostgroup_svc_notifications('linux-servers')
