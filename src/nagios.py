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

from __future__ import with_statement
import func_module
import time

class Nagios(func_module.FuncModule):

    # Update these if need be.
    version = "0.0.1"
    api_version = "0.0.1"
    description = "Run commands like scheduling downtime and enabling or disabling alerts over Func"
    cmdfile = "/var/spool/nagios/cmd/nagios.cmd"

    def _write_command(self, cmd):
        """
        Write the given command to the Nagios command file
        """

        try:
            with open(Nagios.cmdfile, 'w') as fp:
                fp.write(cmd)
        except IOError:
            # TODO: Handle failed writes
            pass

    def schedule_service_downtime(self, host, targets=[], minutes=30):
        """
        Schedule downtime for the target services on host.
        """
        
        dt_start = int(time.time())
        dt_duration = (minutes * 60)
        dt_end = now + dt_duration
        dt_user = "func"
        dt_comment = "Scheduling downtime"
        dt_fixed = 0
        dt_trigger = 0
        
        for service in targets:
            # This kinda sucks but... what can you do...
            #
            # [start_time] SCHEDULE_SVC_DOWNTIME;<host_name>;
            # <service_desription>;<start_time>;<end_time>;<fixed>;
            # <trigger_id>;<duration>;<author>;<comment>
            dt_args = ["SCHEDULE_SVC_DOWNTIME", host, service, dt_start,
                       dt_end, dt_fixed, dt_trigger, dt_duration, dt_user,
                       dt_comment]
            dt_command = "[" + dt_start + "] " + ";".join(dt_args) + "\n"
            self._write_command(dt_command)

    def enable_alerts(self, host):
        """
        Enable alerts on the host.
        """
        pass

    def disable_alerts(self, host):
        """
        Disable alerts on the host.
        """
        pass
