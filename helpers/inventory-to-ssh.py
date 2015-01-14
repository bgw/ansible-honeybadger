# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.

"""Read inventory file, and spit out a list of arguments for the bootstrap
script. This code links rather than shelling out to ansible. That means it must
be licensed under the GPLv3+, and can not inlined with any other Honeybadger
source code, or called directly (without shelling out)."""

from ansible.inventory import Inventory
import argparse

if __name__ != "__main__":
    raise Exception("'%s' may not be imported" % __name__)
parser = argparse.ArgumentParser(description=__doc__)
args = parser.parse_args()

hosts = Inventory().get_hosts()
for h in hosts:
    port = h.get_variables().get("ansible_ssh_port", 22)
    if port != 22:
        print "%s -p %d" % (h.name, port)
    else:
        print h.name
