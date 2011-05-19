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

    def _fmt_dt_str(self, cmd, host, duration, author="func",
                    comment="Scheduling downtime", start=int(time.time()),
                    svc=None, fixed=1, trigger=0):
        """
        Format a downtime external command string.

        cmd - Nagios command ID.
        host - Host schedule downtime on.
        duration - Minutes to schedule downtime for.
        author - Name to file the downtime as.
        comment - Reason for running this command (upgrade, reboot, etc).
        start - Start of downtime in seconds since 12:00AM Jan 1 1970 (Unix epoch).
        svc - Service to schedule downtime for. A value is not required for host downtime.
        fixed - Start now if 1, start when a problem is detected if 0.
        trigger - Optional ID of event to start downtime from. Leave as 0 for fixed downtime.

        Syntax: [start] SCHEDULE_SVC_DOWNTIME;<host_name>;[<service_desription>]
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        # TODO: Make sure this handles flexible downtime correctly. I
        # think flexible triggers downtime for the specified duration
        # when an event is detected in the start-end window.

        # Fmatting the string is not a pretty operation. This is the
        # best I could do whiel still maintaining readability.

        # Header prefixed to the downtime argument string
        hdr = "[%s] %s;%s;" % (start, cmd, host)
        duration_s = (duration * 60)
        end = start + duration_s

        if svc is not None:
            dt_args = [svc, start, end, fixed, trigger,
                       duration_s, author, comment]
        else:
            # Downtime for a host if no svc specified
            dt_args = [start, end, fixed, trigger,
                       duration_s, author, comment]

        dt_arg_str = ";".join(dt_args)
        dt_str = hdr + dt_arg_str

        return dt_str

    def schedule_svc_downtime(self, host, services=[], minutes=30):
        """
        Schedules downtime for a specified service.

        Syntax: SCHEDULE_SVC_DOWNTIME;<host_name>;<service_desription>
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        cmd = "SCHEDULE_SVC_DOWNTIME"
        nagios_return = True

        for service in services:
            dt_cmd_str = self._fmt_dt_str(cmd, host, minutes, svc=service)
            nagios_return = nagios_return and self._write_command(dt_cmd_str)

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

        cmd = "SCHEDULE_HOST_DOWNTIME"
        nagios_return = True
        dt_cmd_str = self._fmt_dt_str(cmd, host, minutes)
	nagios_return = self._write_command(dt_cmd_str)

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

        cmd = "SCHEDULE_HOSTGROUP_HOST_DOWNTIME"
        nagios_return = True
        dt_cmd_str = self._fmt_dt_str(cmd, host, minutes)
	nagios_return = self._write_command(dt_cmd_str)
        pass

    def schedule_hostgroup_svc_downtime(self, hostgroup, minutes=30):
        """
        Schedules downtime for all services associated with hosts in a
        specified servicegroup.

        Syntax: SCHEDULE_HOSTGROUP_SVC_DOWNTIME;<hostgroup_name>;<start_time>;
        <end_time>;<fixed>;<trigger_id>;<duration>;<author>;<comment>

        """

        cmd = "SCHEDULE_HOSTGROUP_SVC_DOWNTIME"
        nagios_return = True
        dt_cmd_str = self._fmt_dt_str(cmd, host, minutes)
	nagios_return = self._write_command(dt_cmd_str)
        pass

    def schedule_servicegroup_host_downtime(self, servicegroup, minutes=30):
        """
        Schedules downtime for all hosts that have services in a
        specified servicegroup.

        Syntax: SCHEDULE_SERVICEGROUP_HOST_DOWNTIME;<servicegroup_name>;
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        cmd = "SCHEDULE_SERVICEGROUP_HOST_DOWNTIME"
        nagios_return = True
        dt_cmd_str = self._fmt_dt_str(cmd, servicegroup, minutes)
	nagios_return = self._write_command(dt_cmd_str)
        pass

    def schedule_servicegroup_svc_downtime(self, servicegroup, minutes=30):
        """
        Schedules downtime for all services in a specified servicegroup.

        Syntax: SCHEDULE_SERVICEGROUP_SVC_DOWNTIME;<servicegroup_name>;
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        cmd = "SCHEDULE_SERVICEGROUP_SVC_DOWNTIME"
        nagios_return = True
        dt_cmd_str = self._fmt_dt_str(cmd, servicegroup, minutes)
	nagios_return = self._write_command(dt_cmd_str)
        pass

    def disable_host_svc_notifications(self, host):
        """
        Disables notifications for all services on the specified host.

        Syntax: DISABLE_HOST_SVC_NOTIFICATIONS;<host_name>
        """

        cmd = "DISABLE_HOST_SVC_NOTIFICATIONS"
        pass

    def disable_host_notifications(self, host):
        """
        Disables notifications for a particular host.

        Syntax: DISABLE_HOST_NOTIFICATIONS;<host_name>
        """

        cmd = "DISABLE_HOST_NOTIFICATIONS"
        pass

    def disable_svc_notifications(self, host, services=[]):
        """
        Disables notifications for a particular service.

        Syntax: DISABLE_SVC_NOTIFICATIONS;<host_name>;<service_description>
        """

        cmd = "DISABLE_SVC_NOTIFICATIONS"
        pass

    def enable_host_notifications(self, host):
        """
        Enables notifications for a particular host.

        Syntax: ENABLE_HOST_NOTIFICATIONS;<host_name>
        """

        cmd = "ENABLE_HOST_NOTIFICATIONS"
        pass

    def enable_host_svc_notifications(self, host):
        """
        Enables notifications for all services on the specified host.

        Syntax: ENABLE_HOST_SVC_NOTIFICATIONS;<host_name>
        """

        cmd = "ENABLE_HOST_SVC_NOTIFICATIONS"
        pass

    def enable_svc_notifications(self, host, service=[]):
        """
        Enables notifications for a particular service.

        Syntax: ENABLE_SVC_NOTIFICATIONS;<host_name>;<service_description>
        """

        cmd = "ENABLE_SVC_NOTIFICATIONS"
        pass

    def enable_hostgroup_host_notifications(self, hostgroup):
        """
        Enables notifications for all hosts in a particular hostgroup.

        Syntax: ENABLE_HOSTGROUP_HOST_NOTIFICATIONS;<hostgroup_name>
        """

        cmd = "ENABLE_HOSTGROUP_HOST_NOTIFICATIONS"
        pass

    def enable_hostgroup_svc_notifications(self, hostgroup):
        """
        Enables notifications for all services that are associated
        with hosts in a particular hostgroup.

        Syntax: ENABLE_HOSTGROUP_SVC_NOTIFICATIONS;<hostgroup_name>
        """

        cmd = "ENABLE_HOSTGROUP_SVC_NOTIFICATIONS"
        pass

    def enable_servicegroup_host_notifications(self, servicegroup):
        """
        Enables notifications for all hosts that have services that
        are members of a particular servicegroup.

        Syntax: ENABLE_SERVICEGROUP_HOST_NOTIFICATIONS;<servicegroup_name>
        """

        cmd = "ENABLE_SERVICEGROUP_HOST_NOTIFICATIONS"
        pass

    def enable_servicegroup_svc_notifications(self, servicegroup):
        """
        Enables notifications for all services that are members of a
        particular servicegroup.

        Syntax: ENABLE_SERVICEGROUP_SVC_NOTIFICATIONS;<servicegroup_name>
        """

        cmd = "ENABLE_SERVICEGROUP_SVC_NOTIFICATIONS"
        pass
