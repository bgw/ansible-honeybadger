Setup on Windows
================

**These instructions aren't very well-tested. Please file an issue about any
positive or negative experience you have with them**

Unfortunately, running ansible-honeybadger on Windows isn't possible. Don't
worry! We can run it directly on your server. This is fine, as long as you're
aware of a few limitations:

-   Backing up the Tor `secret_id_key` automatically isn't possible. This makes
    re-installation more difficult.
-   Deploying to multiple servers at once isn't well supported with this setup.
-   `bootstrap.sh` can't automatically copy your ssh key for you.

Authentication
--------------

Different hosting providers have different authentication mechanisms. AWS uses
ssh RSA keys, providers with SolusVM generate a random root password.

We require you use ssh public-private key authentication as root. [Digital Ocean
has a good writeup on how to generate ssh keys][do rsa].

> Ubuntu's cloud image disables ssh login as root. You can fix this by logging
> in as the 'ubuntu' user, and editing the `/root/.ssh/authorized_keys` file.
>
> Using sudo instead of root makes a lot of sense as a user, but not in the
> context of automated provisioning.

Install
-------

1.  Install [putty].

2.  [Configure putty to use RSA public-private key authentication][do rsa].

3.  Log into your VPS, and execute all further instructions inside that command
    prompt.

4.  Download and run the bootstrap script:

    ```sh
    $ wget https://raw.github.com/pipeep/ansible-honeybadger/master/bootstrap
    $ ./bootstrap localhost
    ```

5.  Clone the git repository

    ```sh
    $ git clone git://github.com/pipeep/ansible-honeybadger.git
    $ cd ansible-honeybadger
    ```

6.  Run the autosetup script, and follow the appropriate prompts:

    ```sh
    $ ./autosetup
    ```

[putty]: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
[do rsa]: https://www.digitalocean.com/community/tutorials/how-to-use-ssh-keys-with-putty-on-digitalocean-droplets-windows-users
