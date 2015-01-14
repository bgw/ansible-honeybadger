Contribution Guidelines
=======================

I ran into a problem during setup. How do I document and share my experience?
-----------------------------------------------------------------------------

Open an issue. We'll try to either get back to you with a workaround, or if
reasonable, extend Honeybadger to handle the issue you ran into.

What can I help with?
---------------------

Of course the most up-to-date place to look is the [issue tracker][]. In
addition to that, we have a number of high-priority, but long-term goals:

-   Improve the `autosetup` experience and add more examples for manual
    configuration.

-   Add more metrics for the running services, such as [`BTCnDash`].

-   Install `nginx-light` on a bitcoin-only box to host the info webpage. As it
    is now, we assume tor will be running on port 80, and so we use tor's
    built-in webserver.

-   We can install new services to an existing Honeybadger host, but right now,
    there's no way to automatically remove services.

[issue tracker]: https://github.com/pipeep/ansible-honeybadger/issues
[`BTCnDash`]: https://pay.reddit.com/r/Bitcoin/comments/26hkbq/

I'd like to add a feature or configuration option to an existing service.
-------------------------------------------------------------------------

Great. Open a PR! These types of changes will likely be easy to merge.

I'd like to add another service.
--------------------------------

This is where things get complicated. We'd love to support X, but first, we need
to guarantee your patches fit in with the rest of the project.

-   Honeybadger is for distributed trustless services. If the service doesn't
    match that model, it's not a good fit for Honeybadger.

-   It shouldn't break anyone's existing Honeybadger install, or if it does, it
    should be [documented appropriately](docs/updating.md).

-   It should be well-documented with examples (see `hosts.example` and
    `host_vars.example`).

-   There should be support for it in the `autosetup` tool.

-   The service binary should be automatically updating, if at all possible, if
    there's an APT repository for this, `unattended-upgrades` will handle that
    for you, otherwise you'll need to write a cron script.

-   If the service crashes, freezes, or dies, it should automatically respawn,
    preferably using monit.

-   The code should be as short and clean as possible, matching the style of
    other existing components.

-   There should be configuration options where we think someone might gain some
    benefit from being able to change the defaults. We tend to err on the side
    of less configurability, because it's easier to add options than to remove
    them.

That doesn't mean you need to finish everything before submitting a pull
request. Open it as soon as you have something working, so we can provide
guidance, and so others can contribute.

### What services are you interested in?

We're currently excited about the possibility of integrating (in order of
increasing perceived difficulty)

-   [I2P](https://geti2p.net/)
-   [btcd](https://github.com/conformal/btcd)
-   [Freenet](https://freenetproject.org/)
-   [Namecoin](https://freenetproject.org/) and other crypto-currency clients
-   [Cjdns](https://github.com/cjdelisle/cjdns)

Open an issue if you'd like to suggest another one, and we may add it to this
list.

How are branches used?
----------------------

We use [feature branches][], and treat master as a stable rolling-release.

[feature branches]: https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow
