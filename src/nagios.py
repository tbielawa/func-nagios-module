# -*- coding: utf-8 -*-
# func-nagios - Schedule downtime and en/disable notifications
# Copyright © 2011, Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license version 2.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

    Examples:

    import func.overlord.client as fc
    nagios_server = fc.Client("nagios.mydomain.com")

    # Schedule 1 hour of downtime for the http service on www01.
    nagios_server.schedule_svc_downtime("www01.ext.mydomain.com",
          services=["http"], minutes=60):

    # Schedule 30 minutes (default) of downtime for the rsync
    # and nfs services on filer05.
    nagios_server.schedule_svc_downtime("filer05.int.mydomain.com",
          services=["rsync", "nfs"]):

    # Schedule 30 minutes (default) of downtime the foobar host.
    nagios_server.schedule_host_downtime("foobar.mydomain.com")

    # Reenable notifications for all services on the foobar host.
    nagios_server.enable_host_svc_notifications("foobar.mydomain.com")

    # Disable notifications for the foo and bar services on the
    # megafrobber host.
    nagios_server.disable_svc_notifications("megafrobber.mydomain.com",
          services=["foo", "bar"])
    """

    version = "0.6.0"
    api_version = "0.6.0"
    description = "Schedule downtime and handle notifications in Nagios."
    cmdfile = "/var/spool/nagios/cmd/nagios.cmd"

    def _write_command(self, cmd):
        """
        Write the given command to the Nagios command file
        """

        print cmd
        return True

        # try:
        #     fp = open(Nagios.cmdfile, 'w')
        #     fp.write(cmd)
        #     fp.flush()
        #     fp.close()
        #     return True
        # except IOError:
        #     return False

    def _fmt_dt_str(self, cmd, host, duration, author="func",
                    comment="Scheduling downtime", start=int(time.time()),
                    svc=None, fixed=1, trigger=0):
        """
        Format a downtime external-command string.

        cmd - Nagios command ID.
        host - Host schedule downtime on.
        duration - Minutes to schedule downtime for.
        author - Name to file the downtime as.
        comment - Reason for running this command (upgrade, reboot, etc).
        start - Start of downtime in seconds since 12:00AM Jan 1 1970 (Unix epoch).
        svc - Service to schedule downtime for. A value is not required 
          for host downtime.
        fixed - Start now if 1, start when a problem is detected if 0.
        trigger - Optional ID of event to start downtime from. Leave as 0 for
          fixed downtime.

        Syntax: [submitted] COMMAND;<host_name>;[<service_desription>]
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

    def _fmt_notif_str(self, cmd, host, svc=None):
        """
        Format a notification external-command string.

        cmd - Nagios command ID.
        host - Host to en/disable notifications on..
        svc - Service to schedule downtime for. A value is not required
          for host downtime.

        Syntax: [submitted] COMMAND;<host_name>[;<service_description>]
        """

        submitted = int(time.time())

        if svc is not None:
            notif_str = "[%s] %s;%s;%s" % (submitted, cmd, host, svc)
        else:
            # Downtime for a host if no svc specified
            notif_str = "[%s] %s;%s" % (submitted, cmd, host)

        return notif_str

    def schedule_svc_downtime(self, host, services=[], minutes=30):
        """
        This command is used to schedule downtime for a particular
        service.

        During the specified downtime, Nagios will not send
        notifications out about the service.

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
        This command is used to schedule downtime for a particular
        host.

        During the specified downtime, Nagios will not send
        notifications out about the host.

        Syntax: SCHEDULE_HOST_DOWNTIME;<host_name>;<start_time>;<end_time>;<fixed>;
        <trigger_id>;<duration>;<author>;<comment>
        """

        cmd = "SCHEDULE_HOST_DOWNTIME"
        dt_cmd_str = self._fmt_dt_str(cmd, host, minutes)
	nagios_return = self._write_command(dt_cmd_str)

        if nagios_return:
            return "OK"
        else:
            return "Fail: could not write to command file"

    def schedule_hostgroup_host_downtime(self, hostgroup, minutes=30):
        """
        This command is used to schedule downtime for all hosts in a
        particular hostgroup.

        During the specified downtime, Nagios will not send
        notifications out about the hosts.

        Syntax: SCHEDULE_HOSTGROUP_HOST_DOWNTIME;<hostgroup_name>;<start_time>;
        <end_time>;<fixed>;<trigger_id>;<duration>;<author>;<comment>
        """

        cmd = "SCHEDULE_HOSTGROUP_HOST_DOWNTIME"
        dt_cmd_str = self._fmt_dt_str(cmd, host, minutes)
	nagios_return = self._write_command(dt_cmd_str)

    def schedule_hostgroup_svc_downtime(self, hostgroup, minutes=30):
        """
        This command is used to schedule downtime for all services in
        a particular hostgroup.

        During the specified downtime, Nagios will not send
        notifications out about the services.

        Note that scheduling downtime for services does not
        automatically schedule downtime for the hosts those services
        are associated with.

        Syntax: SCHEDULE_HOSTGROUP_SVC_DOWNTIME;<hostgroup_name>;<start_time>;
        <end_time>;<fixed>;<trigger_id>;<duration>;<author>;<comment>
        """

        cmd = "SCHEDULE_HOSTGROUP_SVC_DOWNTIME"
        dt_cmd_str = self._fmt_dt_str(cmd, hostgroup, minutes)
	nagios_return = self._write_command(dt_cmd_str)

    def schedule_servicegroup_host_downtime(self, servicegroup, minutes=30):
        """
        This command is used to schedule downtime for all hosts in a
        particular servicegroup.

        During the specified downtime, Nagios will not send
        notifications out about the hosts.

        Syntax: SCHEDULE_SERVICEGROUP_HOST_DOWNTIME;<servicegroup_name>;
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        cmd = "SCHEDULE_SERVICEGROUP_HOST_DOWNTIME"
        dt_cmd_str = self._fmt_dt_str(cmd, servicegroup, minutes)
	nagios_return = self._write_command(dt_cmd_str)

    def schedule_servicegroup_svc_downtime(self, servicegroup, minutes=30):
        """
        This command is used to schedule downtime for all services in
        a particular servicegroup.

        During the specified downtime, Nagios will not send
        notifications out about the services.

        Note that scheduling downtime for services does not
        automatically schedule downtime for the hosts those services
        are associated with.

        Syntax: SCHEDULE_SERVICEGROUP_SVC_DOWNTIME;<servicegroup_name>;
        <start_time>;<end_time>;<fixed>;<trigger_id>;<duration>;<author>;
        <comment>
        """

        cmd = "SCHEDULE_SERVICEGROUP_SVC_DOWNTIME"
        dt_cmd_str = self._fmt_dt_str(cmd, servicegroup, minutes)
	nagios_return = self._write_command(dt_cmd_str)

    def disable_host_svc_notifications(self, host):
        """
        This command is used to prevent notifications from being sent
        out for all services on the specified host.

        Note that this command does not disable notifications from
        being sent out about the host.

        Syntax: DISABLE_HOST_SVC_NOTIFICATIONS;<host_name>
        """

        cmd = "DISABLE_HOST_SVC_NOTIFICATIONS"
        notif_str = self._fmt_notif_str(cmd, host)
	nagios_return = self._write_command(notif_str)

    def disable_host_notifications(self, host):
        """
        This command is used to prevent notifications from being sent
        out for the specified host.

        Note that this command does not disable notifications for
        services associated with this host.

        Syntax: DISABLE_HOST_NOTIFICATIONS;<host_name>
        """

        cmd = "DISABLE_HOST_NOTIFICATIONS"
        notif_str = self._fmt_notif_str(cmd, host)
	nagios_return = self._write_command(notif_str)

    def disable_svc_notifications(self, host, services=[]):
        """
        This command is used to prevent notifications from being sent
        out for the specified service.

        Note that this command does not disable notifications from
        being sent out about the host.

        Syntax: DISABLE_SVC_NOTIFICATIONS;<host_name>;<service_description>
        """

        cmd = "DISABLE_SVC_NOTIFICATIONS"
        nagios_return = True
        for service in services:
            notif_str = self._fmt_notif_str(cmd, host, svc=service)
            nagios_return = nagios_return and self._write_command(notif_str)

    def disable_servicegroup_host_notifications(self, servicegroup):
        """
        This command is used to prevent notifications from being sent
        out for all hosts in the specified servicegroup.

        Note that this command does not disable notifications for
        services associated with hosts in this service group.

        Syntax: DISABLE_SERVICEGROUP_HOST_NOTIFICATIONS;<servicegroup_name>
        """

        cmd = "DISABLE_SERVICEGROUP_HOST_NOTIFICATIONS"
        nagios_return = self._fmt_notif_str(cmd, servicegroup)

    def disable_servicegroup_svc_notifications(self, servicegroup):
        """
        This command is used to prevent notifications from being sent
        out for all services in the specified servicegroup.

        Note that this does not prevent notifications from being sent
        out about the hosts in this servicegroup.

        Syntax: DISABLE_SERVICEGROUP_SVC_NOTIFICATIONS;<servicegroup_name>
        """

        cmd = "DISABLE_SERVICEGROUP_SVC_NOTIFICATIONS"
        nagios_return = self._fmt_n(cmd, servicegroup)

    def disable_hostgroup_host_notifications(self, hostgroup):
        """
        Disables notifications for all hosts in a particular
        hostgroup.

        Note that this does not disable notifications for the services
        associated with the hosts in the hostgroup - see the
        DISABLE_HOSTGROUP_SVC_NOTIFICATIONS command for that.

        Syntax: DISABLE_HOSTGROUP_HOST_NOTIFICATIONS;<hostgroup_name>
        """

        cmd = "DISABLE_HOSTGROUP_HOST_NOTIFICATIONS"
        nagios_return = self._fmt_n(cmd, servicegroup)

    def disable_hostgroup_svc_notifications(self, hostgroup):
        """
        Disables notifications for all services associated with hosts
        in a particular hostgroup.

        Note that this does not disable notifications for the hosts in
        the hostgroup - see the DISABLE_HOSTGROUP_HOST_NOTIFICATIONS
        command for that.

        Syntax: DISABLE_HOSTGROUP_SVC_NOTIFICATIONS;<hostgroup_name>
        """

        cmd ="DISABLE_HOSTGROUP_SVC_NOTIFICATIONS"
        nagios_return = self._fmt_n(cmd, servicegroup)

    def enable_host_notifications(self, host):
        """
        Enables notifications for a particular host.

        Note that this command does not enable notifications for
        services associated with this host.

        Syntax: ENABLE_HOST_NOTIFICATIONS;<host_name>
        """

        cmd = "ENABLE_HOST_NOTIFICATIONS"
        notif_str = self._fmt_notif_str(cmd, host)
	nagios_return = self._write_command(notif_str)

    def enable_host_svc_notifications(self, host):
        """
        Enables notifications for all services on the specified host.

        Note that this does not enable notifications for the host.

        Syntax: ENABLE_HOST_SVC_NOTIFICATIONS;<host_name>
        """

        cmd = "ENABLE_HOST_SVC_NOTIFICATIONS"
        notif_str = self._fmt_notif_str(cmd, host)
	nagios_return = self._write_command(notif_str)

    def enable_svc_notifications(self, host, services=[]):
        """
        Enables notifications for a particular service.

        Note that this does not enable notifications for the host.

        Syntax: ENABLE_SVC_NOTIFICATIONS;<host_name>;<service_description>
        """

        cmd = "ENABLE_SVC_NOTIFICATIONS"
        nagios_return = True
        for service in services:
            notif_str = self._fmt_notif_str(cmd, host, svc=service)
            nagios_return = nagios_return and self._write_command(notif_str)

    def enable_hostgroup_host_notifications(self, hostgroup):
        """
        Enables notifications for all hosts in a particular hostgroup.

        Note that this command does not enable notifications for
        services associated with the hosts in this hostgroup.

        Syntax: ENABLE_HOSTGROUP_HOST_NOTIFICATIONS;<hostgroup_name>
        """

        cmd = "ENABLE_HOSTGROUP_HOST_NOTIFICATIONS"
        notif_str = self._fmt_notif_str(cmd, hostgroup)
	nagios_return = self._write_command(notif_str)

    def enable_hostgroup_svc_notifications(self, hostgroup):
        """
        Enables notifications for all services that are associated
        with hosts in a particular hostgroup.

        Note that this does not enable notifications for the hosts in
        this hostgroup.

        Syntax: ENABLE_HOSTGROUP_SVC_NOTIFICATIONS;<hostgroup_name>
        """

        cmd = "ENABLE_HOSTGROUP_SVC_NOTIFICATIONS"
        notif_str = self._notif_str(cmd, hostgroup)
	nagios_return = self._write_command(notif_str)

    def enable_servicegroup_host_notifications(self, servicegroup):
        """
        Enables notifications for all hosts that have services that
        are members of a particular servicegroup.

        Note that this command does not enable notifications for
        services associated with the hosts in this servicegroup.

        Syntax: ENABLE_SERVICEGROUP_HOST_NOTIFICATIONS;<servicegroup_name>
        """

        cmd = "ENABLE_SERVICEGROUP_HOST_NOTIFICATIONS"
        notif_str = self._fmt_notif_str(cmd, servicegroup)
	nagios_return = self._write_command(notif_str)

    def enable_servicegroup_svc_notifications(self, servicegroup):
        """
        Enables notifications for all services that are members of a
        particular servicegroup.

        Note that this does not enable notifications for the hosts in
        this servicegroup.

        Syntax: ENABLE_SERVICEGROUP_SVC_NOTIFICATIONS;<servicegroup_name>
        """

        cmd = "ENABLE_SERVICEGROUP_SVC_NOTIFICATIONS"
        notif_str = self._fmt_notif_str(cmd, servicegroup)
	nagios_return = self._write_command(notif_str)


