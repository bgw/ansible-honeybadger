"""
Interactively prompts about basic configuration settings, and writes them to the
relevant locations in the CWD.

I know this code is messy as hell. I just wanted to get a release out.
"""

from __future__ import print_function

if __name__ != "__main__":
    raise Exception("'%s' may not be imported" % __name__)

import argparse
import functools
import inquirer
import os
import os.path
import re
import socket
import sys
import traceback
import yaml

from blessings import Terminal
from collections import OrderedDict

terminal = Terminal()

def print_err(*args, **kwargs):
    print("{t.bold}{t.white}{t.on_red}".format(t=terminal),
          file=sys.stderr, end="")
    print(*args, file=sys.stderr, **kwargs)
    print("{t.normal}".format(t=terminal), file=sys.stderr, end="")

def prompt():
    hosts = {}

    questions = [
        inquirer.List("location",
                      "Where are we setting up honeybadger on?",
                      choices=["One or more remote servers (ssh, recommended)",
                               "This machine (localhost)"]),
    ]
    local = "localhost" in inquirer.prompt(questions)["location"]

    prev = {}
    while True:
        h = prompt_host(local, prev)
        hosts[h.pop("name")] = h
        prev = h
        if local or not another():
            break
    return hosts

def prompt_host(local=False, prev={}):
    supported_services = ["bitcoind", "tor"]
    questions = [
        inquirer.Text("name",
                      "DNS name or IP address",
                      validate=validate_host,
                      default="localhost" if local else None),
        inquirer.Text("ansible_ssh_port",
                      "[{name}] SSH port",
                      default=str(prev.get("ansible_ssh_port", "22")),
                      validate=validate_tcp_port,
                      ignore=local),
    ]
    answers = inquirer.prompt(questions, answers={"local": local})
    answers = transform_value(answers, "ansible_ssh_port", int)

    # Select services
    while True:
        questions = [
            inquirer.Checkbox("services",
                              "[{name}] Services to enable",
                              choices=supported_services,
                              validate=lambda _, s: s),
            inquirer.Confirm("is_unmetered",
                             message="[{name}] Is this an unmetered plan?"),
            inquirer.Confirm("continue",
                             message="[{name}] We can't rate-limit bitcoind "
                             "yet. Continue anyways?",
                             default=True,
                             ignore=lambda a: a["is_unmetered"] or
                                              "bitcoind" not in a["services"]),
        ]
        answers = inquirer.prompt(questions, answers=answers)
        if answers["continue"]:
            del answers["continue"]
            break

    # transform answers
    for service in supported_services:
        answers[service] = service in answers["services"]
    del answers["services"]

    if answers["tor"]:
        questions = [
            inquirer.Text("tor_nickname",
                          "[{name}] Tor relay nickname (letters and numbers)",
                          default=prev.get("tor_nickname", "honeybadger"),
                          validate=validate_tor_nickname),
            inquirer.Text("tor_contact_info",
                          "[{name}] Tor contact info "
                          "(you may obfusicate this)",
                          default=prev.get("tor_contact_info")),
            inquirer.Text("tor_address",
                          "[{name}] Tor bind address (leave blank to skip)",
                          default=prev.get("tor_address"),
                          validate=validate_or_blank(validate_host)),
            inquirer.Text("tor_or_port",
                          "[{name}] Tor relay TCP port",
                          default=str(prev.get("tor_or_port", "443")),
                          validate=validate_tcp_port),
            inquirer.Text("tor_dir_port",
                          "[{name}] Tor directory TCP port",
                          default=str(prev.get("tor_dir_port", "80")),
                          validate=validate_tcp_port),
            inquirer.Text("tor_bandwidth_rate",
                          "[{name}] Average bandwidth per second "
                          "(eg. '75 KBytes')",
                          default=prev.get("tor_bandwidth_rate"),
                          ignore=lambda a: a["is_unmetered"],
                          validate=validate_tor_bandwidth),
            inquirer.Text("tor_bandwidth_burst",
                          "[{name}] Max burst bandwidth per second "
                          "(eg. '125 KBytes')",
                          default=prev.get("tor_bandwidth_burst"),
                          ignore=lambda a: a["is_unmetered"],
                          validate=validate_tor_bandwidth),
        ]
        answers = inquirer.prompt(questions, answers=answers)
        answers = transform_value(answers, "tor_or_port", "tor_dir_port", int)

    if answers["bitcoind"]:
        questions = [
            inquirer.Text("bitcoind_address",
                          "[{name}] Bitcoind bind address (leave blank to "
                          "skip)",
                          default=prev.get("tor_address"),
                          validate=validate_or_blank(validate_host)),
            inquirer.Text("bitcoind_port",
                          "[{name}] Bitcoind TCP port",
                          default=str(prev.get("bitcoind_port", "8333")),
                          validate=validate_tcp_port),
            inquirer.Text("bitcoind_maxconnections",
                          "[{name}] Bitcoind maximum incoming connections",
                          default="125",
                          validate=lambda _, n: 0 <= long(n) < 10000),
        ]
        answers = inquirer.prompt(questions, answers=answers)
        answers = transform_value(answers, "bitcoind_port", int)
        answers = transform_value(answers, "bitcoind_maxconnections", int)

    questions = [
        inquirer.Text("www_port",
                      "[{name}] Port to run informational web server on",
                      default=str(prev.get("www_port", "80")),
                      validate=validate_www_port),
        inquirer.Text("www_donations",
                      "[{name}] Donation message (leave blank to skip)",
                      default=prev.get("www_donations")),
    ]
    answers = inquirer.prompt(questions, answers=answers)
    answers = transform_value(answers, "www_port", int)

    if answers["tor"] and answers["www_port"] == answers["tor_dir_port"]:
        # determine a sensible bitcoind_rpc_port
        p = auto_tcp_port(answers, 9030)
        if p != 9030: # otherwise, let it be implicit
            answers["tor_proxied_dir_port"] = p
    if answers["bitcoind"]:
        # determine a sensible bitcoind_rpc_port
        p = auto_tcp_port(answers, 8332)
        if p != 8332: # otherwise, let it be implicit
            answers["bitcoind_rpc_port"] = p

    # transform answers
    def auto_del(answers, k, *args):
        """Delete empty answers, allowing the defaults to take over. If a
        default is given, the value is deleted if it matches the default. If a
        default is not given, the value is deleted if it is falsy."""
        try:
            if args:
                if answers[k] == args[0]:
                    del answers[k]
            elif not answers[k]:
                del answers[k]
        except KeyError:
            pass
        return answers

    del answers["is_unmetered"]
    auto_del(answers, "bitcoind_address")
    auto_del(answers, "bitcoind_maxconnections", 125)
    auto_del(answers, "bitcoind_port", 8333)
    auto_del(answers, "tor_address")
    auto_del(answers, "tor_bandwidth_burst")
    auto_del(answers, "tor_bandwidth_rate")
    auto_del(answers, "tor_contact_info")
    auto_del(answers, "tor_dir_port", 80)
    auto_del(answers, "tor_or_port", 443)
    auto_del(answers, "www_donations")
    auto_del(answers, "www_port", 80)

    return answers

def auto_tcp_port(answers, desired):
    """Starting with a desired port, try every possible tcp port until we find a
    free one, and return that one."""
    port = desired
    while True:
        if port not in get_used_ports(answers):
            break
        port += 1
    return port

def validate_host(_, h):
    """Raises socket.gaierror if the host doesn't exist"""
    return socket.getaddrinfo(h, 0)

def validate_port(_, p):
    """Ensure the port number if in the valid range."""
    return 0 < long(p) < 2**16

def validate_tor_nickname(_, nick):
    return re.match(r"^[a-zA-Z0-9]{1,20}$", nick)

def validate_tor_bandwidth(_, bw):
    try:
        n, unit = bw.split(" ")
        unit = unit.lower()
        prefix, suffix = re.match(r"^(.+)(bits?|bytes?|b)$", unit).groups()
        return long(n) > 0 and \
            prefix in ["k", "m", "g", "t", "kilo", "mega", "giga", "tera"]
    except ex:
        print(ex)

def get_used_ports(answers):
    places = "ansible_ssh_port", "tor_or_port", "tor_dir_port", "bitcoind_port"
    used = set(int(answers.get(p, 0)) for p in places)
    used.discard(0)
    return used

def validate_tcp_port(answers, port):
    "Run validate_port and ensure the current port hasn't already been used."
    return validate_port(answers, port) and \
        int(port) not in get_used_ports(answers)

def validate_www_port(answers, port):
    "The www port can intersect with tor_dir_port, but nothing else."
    return validate_port(answers, port) and (
        int(port) not in get_used_ports(answers) or
            int(port) == answers["tor_dir_port"]
    )

def validate_or_blank(f):
    """Decorator for a validator that also accepts blank values"""
    @functools.wraps(f)
    def wrapper(answers, value):
        return True if value == "" else f(answers, value)
    return wrapper

def transform_value(answers, *args):
    answers = dict(answers)
    keys = args[:-1]
    f = args[-1]
    for k in keys:
        answers[k] = f(answers[k])
    return answers

def another():
    questions = [inquirer.Confirm("another", message="Add another server")]
    return inquirer.prompt(questions)["another"]

def pretty_yaml(data, *args, **kwargs):
    def order_rep(dumper, data):
        return dumper.represent_mapping("tag:yaml.org,2002:map", data.items(),
                                        flow_style=False)
    yaml.add_representer(OrderedDict, order_rep)
    def order(data):
        if isinstance(data, dict):
            dict((k, order(v)) for (k, v) in data.items())
            data = OrderedDict(sorted(data.items()))
        return data
    yaml.add_representer(OrderedDict, order_rep)
    kwargs["default_flow_style"] = False
    return yaml.dump(order(data), *args, **kwargs)

def write_config(hosts, dry=False):
    inventory = []
    for host, config in hosts.items():
        config = dict(config) # we're going to be making modifications
        if config.get("local", False):
            inventory.append("%s ansible_connection=local" % host)
        elif config.get("ansible_ssh_port", 22) != 22:
            inventory.append("%s ansible_ssh_port=%d" %
                             (host, config["ansible_ssh_port"]))
        else:
            inventory.append(host)
        del config["local"]
        config.pop("ansible_ssh_port", None) # might not be defined

        if dry:
            print("---")
            print("# host_vars/%s.yml:" % host)
            print(pretty_yaml(config))
        else:
            if not os.path.exists("host_vars"):
                os.makedirs("host_vars")
            with open("host_vars/%s.yml" % host, "w") as fp:
                fp.write("---")
                fp.write(pretty_yaml(config))
                fp.write("\n")

    if dry:
        print("---")
        print("# hosts")
        print("\n".join(inventory))
    else:
        with open("hosts", "w") as fp:
            fp.write("\n".join(inventory))
            fp.write("\n")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--dry", action="store_true",
                    help="Don't write any files, but instead print out what "
                         "would've been written")
args = parser.parse_args()

try:
    config = prompt()
except KeyboardInterrupt:
    print()
    print_err("Exiting. No configuration has been written.")
    sys.exit(1)
except:
    traceback.print_exc()
    print_err("We encountered an error. No configuration has been written.")
    sys.exit(1)
write_config(config, dry=args.dry)
