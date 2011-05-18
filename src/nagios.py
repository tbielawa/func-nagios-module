#
# Copyright 2011
# Tim Bielawa <tbielawa@redhat.com>
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import func_module
import time

class Nagios(func_module.FuncModule):
    """
    Perform common tasks in Nagios related to downtime and
    notifications.

    The complete set of external commands Nagios handles is documented
    on their website:
    
    http://old.nagios.org/developerinfo/externalcommands/commandlist.php

    This module differs from the standard external command API in that
    methods that operate on specific services expect a list of
    services. This deviation is so operations on subsets of a given
    hosts services can be performed in one call.
    """

    version = "0.5.1"
    api_version = "0.5.1"
    description = "Run commands like scheduling downtime and enabling or disabling alerts over Func"
    cmdfile = "/var/spool/nagios/cmd/nagios.cmd"

    def _write_command(self, cmd):
        """
        Write the given command to the Nagios command file
        """

        try:
            fp = open(Nagios.cmdfile, 'w')
            fp.write(cmd)
            fp.flush()
            fp.close()
            return True
        except IOError:
            return False

    def schedule_svc_downtime(self, host, services=[], minutes=30):
        """
        Schedules downtime for a specified service.

        Syntax: SCHEDULE_SVC_DOWNTIME;<host_name>;<service_desription>
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        dt_start = int(time.time())
        dt_duration = (minutes * 60)
        dt_end = dt_start + dt_duration
        dt_user = "func"
        dt_comment = "Scheduling downtime"
        dt_fixed = 1
        dt_trigger = 0

        nagios_return = True

        for service in targets:
            # This is kinda ugly and sucky but... what can you do...
            dt_args = ["SCHEDULE_SVC_DOWNTIME", host, service, str(dt_start),
                       str(dt_end), str(dt_fixed), str(dt_trigger), str(dt_duration), dt_user,
                       dt_comment]
            dt_command = "[" + str(dt_start) + "] " + ";".join(dt_args) + "\n"
            nagios_return = nagios_return and self._write_command(dt_command)

        if nagios_return:
            return "OK"
        else:
            return "Fail: could not write to command file"

    def schedule_host_downtime(self, host, minutes=30):
        """
        Schedules downtime for a specified host.
 
        Syntax: SCHEDULE_HOST_DOWNTIME;<host_name>;<start_time>;<end_time>;<fixed>;
        <trigger_id>;<duration>;<author>;<comment>
        """

        dt_start = int(time.time())
        dt_duration = (minutes * 60)
        dt_end = dt_start + dt_duration
        dt_user = "func"
        dt_comment = "Scheduling downtime"
        dt_fixed = 1
        dt_trigger = 0
        dt_args = ["SCHEDULE_HOST_DOWNTIME", host, str(dt_start), str(dt_end), 
                   str(dt_fixed), str(dt_trigger), str(dt_duration), dt_user, 
                   dt_comment]

        nagios_return = True

        dt_command = "[" + str(dt_start) + "] " + ";".join(dt_args)
        nagios_return = self._write_command(dt_command)

        if nagios_return:
            return "OK"
        else:
            return "Fail: could not write to command file"

    def schedule_hostgroup_host_downtime(self, hostgroup, minutes=30):
        """
        Schedules downtime for all hosts in a specified hostgroup.

        Syntax: SCHEDULE_HOSTGROUP_HOST_DOWNTIME;<hostgroup_name>;<start_time>;
        <end_time>;<fixed>;<trigger_id>;<duration>;<author>;<comment>
        """

        pass

    def schedule_hostgroup_svc_downtime(self, hostgroup, minutes=30):
        """
        Schedules downtime for all services associated with hosts in a
        specified servicegroup.

        Syntax: SCHEDULE_HOSTGROUP_SVC_DOWNTIME;<hostgroup_name>;<start_time>;
        <end_time>;<fixed>;<trigger_id>;<duration>;<author>;<comment>

        """

        pass

    def schedule_servicegroup_host_downtime(self, servicegroup, minutes=30):
        """
        Schedules downtime for all hosts that have services in a
        specified servicegroup.

        Syntax: SCHEDULE_SERVICEGROUP_HOST_DOWNTIME;<servicegroup_name>;
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        pass

    def schedule_servicegroup_svc_downtime(self, servicegroup, minutes=30):
        """
        Schedules downtime for all services in a specified servicegroup.

        Syntax: SCHEDULE_SERVICEGROUP_SVC_DOWNTIME;<servicegroup_name>;
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        pass

    def disable_host_svc_notifications(self, host):
        """
        Disables notifications for all services on the specified host.

        Syntax: DISABLE_HOST_SVC_NOTIFICATIONS;<host_name>
        """

        pass

    def disable_host_notifications(self, host):
        """
        Disables notifications for a particular host.

        Syntax: DISABLE_HOST_NOTIFICATIONS;<host_name>
        """

        pass

    def disable_svc_notifications(self, host, services=[]):
        """
        Disables notifications for a particular service.

        Syntax: DISABLE_SVC_NOTIFICATIONS;<host_name>;<service_description>
        """

        pass


    def enable_host_notifications(self, host):
        """
        Enables notifications for a particular host.

        Syntax: ENABLE_HOST_NOTIFICATIONS;<host_name>
        """

        pass

    def enable_host_svc_notifications(self, host):
        """
        Enables notifications for all services on the specified host.

        Syntax: ENABLE_HOST_SVC_NOTIFICATIONS;<host_name>
        """

        pass


    def enable_svc_notifications(self, host, service=[]):
        """
        Enables notifications for a particular service.

        Syntax: ENABLE_SVC_NOTIFICATIONS;<host_name>;<service_description>
        """

        pass

    def enable_hostgroup_host_notifications(self, hostgroup):
        """
        Enables notifications for all hosts in a particular hostgroup.

        Syntax: ENABLE_HOSTGROUP_HOST_NOTIFICATIONS;<hostgroup_name>
        """

        pass

    def enable_hostgroup_svc_notifications(self, hostgroup):
        """
        Enables notifications for all services that are associated
        with hosts in a particular hostgroup.

        Syntax: ENABLE_HOSTGROUP_SVC_NOTIFICATIONS;<hostgroup_name>
        """

        pass

    def enable_servicegroup_host_notifications(self, servicegroup):
        """
        Enables notifications for all hosts that have services that
        are members of a particular servicegroup.

        Syntax: ENABLE_SERVICEGROUP_HOST_NOTIFICATIONS;<servicegroup_name>
        """

        pass

    def enable_servicegroup_svc_notifications(self, servicegroup):
        """
        Enables notifications for all services that are members of a
        particular servicegroup.

        Syntax: ENABLE_SERVICEGROUP_SVC_NOTIFICATIONS;<servicegroup_name>
        """

        pass
