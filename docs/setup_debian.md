Setup on Debian or Ubuntu
=========================

These directions assume you're using a Debian or Ubuntu desktop for deployment.
**These instructions assume you're on a separate machine from the server.**

Authentication
--------------

Different hosting providers have different authentication mechanisms. AWS uses
ssh RSA keys, providers with SolusVM generate a random root password.

We require you use ssh public-private key authentication as root. If you have a
key already, you're good to go. We'll ask for your password and use
`ssh-copy-id` to copy it to the server for you.

[GitHub has a good writeup on how to generate ssh keys][git rsa]. If you follow
their guide, you only need to complete the first two steps. We'll copy it to
your server for you.

[git rsa]: https://help.github.com/articles/generating-ssh-keys/#platform-linux

> Ubuntu's cloud image disables ssh login as root. You can fix this by logging
> in as the 'ubuntu' user, and editing the `/root/.ssh/authorized_keys` file.
>
> Using sudo instead of root makes a lot of sense as a user, but not in the
> context of automated provisioning.

Install
-------

1.  Install our dependencies:

    ```sh
    $ sudo aptitude install python python-pip   # alternatively, apt-get install
    $ sudo pip install virtualenv
    ```

    > In place of using the version from pip, you can use Debian's
    > python-virtualenv package.

2.  Clone the git repository

    ```sh
    $ git clone git://github.com/pipeep/ansible-honeybadger.git
    $ cd ansible-honeybadger
    ```

3.  Run the autosetup script, and follow the appropriate prompts:

    ```sh
    $ ./autosetup
    ```
