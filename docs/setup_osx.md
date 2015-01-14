Setup on Mac OS X
=================

**These instructions aren't very well-tested. Please file an issue about any
positive or negative experience you have with them**

These directions assume you're using a Mac OS X desktop for deployment. These
instructions should *not* be run on the server.

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

[git rsa]: https://help.github.com/articles/generating-ssh-keys/#platform-mac

> Ubuntu's cloud image disables ssh login as root. You can fix this by logging
> in as the 'ubuntu' user, and editing the `/root/.ssh/authorized_keys` file.
>
> Using sudo instead of root makes a lot of sense as a user, but not in the
> context of automated provisioning.

Install
-------

1.  OS X comes with Python, but it's an old version, and you may prefer to use
    the version from homebrew:

    ```sh
    $ sudo brew install python
    ```

2.  If you don't have `pip` (homebrew's package will install it for you), you
    can install it with:

    ```sh
    $ sudo easy_install pip
    ```

3.  If you don't already have `virtualenv`, you can install it with:

    ```sh
    $ sudo pip install virtualenv
    ```

4.  Clone the git repository

    ```sh
    $ git clone git://github.com/pipeep/ansible-honeybadger.git
    $ cd ansible-honeybadger
    ```

5.  Run the autosetup script, and follow the appropriate prompts:

    ```sh
    $ ./autosetup
    ```
