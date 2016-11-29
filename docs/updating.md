Updating Honeybadger
====================

In general, updating should be as easy as running

```
git pull
./autosetup --no-config
```

In case it's not, we'll update this document with what you need to do to get
from revision A to revision B. **Check this document first** before updating
your Honeybadger install.

We hope to script this in the future to have an easier update process, akin to
`autosetup`.

November 28th, 2016
-------------------

Honeybadger now requires Ubuntu 16.04 (it previously depended on 14.04). This
brings a large amount of improvements. For example, tor is able to take
advantage of systemd's additional sandboxing support, so a compromised tor
daemon would have less effect on the system's security as a whole.

Because this is a major upgrade, you shouldn't attempt to upgrade the machine
in-place. Instead, simply wipe the VM, install Ubuntu 16.04, and re-run
honeybadger.

bitcoind will need to re-download the entire blockchain (which can take a
while), but honeybadger will preserve tor secrets across installs, so your tor
relay's fingerprint will not change. This is important for preserving your
relay's reputation. On a fresh install, honeybadger will look for the backup of
this key in `ansible-honeybadger/secrets/tor/example.com_secret_id_key`.

No configuration options have been changed as a result of this release.
