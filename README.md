What is This?
=============

![Travis CI](https://travis-ci.org/zaufi/pluggable-output-processor.svg?branch=master)

_Pluggable Output Processor_ is an engine to wrap any executabe and capture its output through
a pluggable module to colorize it and/or (re)format.


Features
--------

* easy (to Python programmers ;-) to extend
* 256 color terminal support ;-) configuration files in addition to standard named colors
  may contain color definitions as `rgb(r,g,b)` or `gray(n)`
* colorizers for `make`, `cmake`, `gcc` out of the box (more to come ;-)
* some modules are not just a stupid colorizers ;-) For example `gcc` can reformat text for
  better readability (really helps to understand template errors). Also `cmake` module can reduce
  amount of lines printed during test by collapsing test _intro_ message and _result_ into a single one.


Installation
------------

Easy!

    $ pip install outproc

For Gentoo users there is a [live ebuild][raw-ebuild] in my [repository][my-overlay].
Also (for Gentoo users again ;-) `eselect` module from `contrib/` will be installed by the ebuild.
Users of other distros have to make symlinks to required modules manually:

    $ ln -s /usr/bin/outproc /usr/lib/outproc/bin/<module-name>

and then make sure `/usr/lib/outproc/bin` placed __before__ `/usr/bin` (and anything else) in your
user/system `PATH` environment. Available modules (plugins) can be found at `<python-site-packages-dir>/outproc/pp`.
For example, to install the `gcc` module do the following:

    $ ln -s /usr/bin/outproc /usr/lib/outproc/bin/gcc

Then you may edit `/etc/outproc/gcc.conf` to adjust color settings.

[raw-ebuild]: https://github.com/zaufi/zaufi-overlay/blob/master/dev-util/pluggable-output-processor/pluggable-output-processor-scm.ebuild
[my-overlay]: https://github.com/zaufi/zaufi-overlay/ "My ebuilds overlay"
