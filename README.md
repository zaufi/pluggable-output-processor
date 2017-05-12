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
Users of other distros have to make symlinks to required modules manually (replace `<install-prefix>`
with your actual path):

    $ ln -s <install-prefix>/bin/outproc /usr/lib/outproc/bin/<module-name>

and then make sure `/usr/lib/outproc/bin` placed __before__ `/usr/bin` (and anything else) in your
user/system `PATH` environment. The path `/usr/lib/outproc/bin` is just an example. You can choose
whatever you like instead (e.g. `/home/<login>/.local/bin/` for user based install layout).
List of available modules (plugins) can be obtained from command:

    $ outproc -l
    List of available modules:
      c++
      cc
      cmake
      diff
      g++
      gcc
      make
      mount

For example, to install the `make` module do the following:

    $ ln -s <install-prefix>/bin/outproc /usr/lib/outproc/bin/make

Then you may edit `/etc/outproc/make.conf` to adjust color settings. Note that `gcc`, `g++`, `cc` and `c++`
are the same module actually (named after typical GCC executables) and use the same `/etc/outproc/gcc.conf`
config file.

[raw-ebuild]: https://github.com/zaufi/zaufi-overlay/blob/master/dev-util/pluggable-output-processor/pluggable-output-processor-scm.ebuild
[my-overlay]: https://github.com/zaufi/zaufi-overlay/ "My ebuilds overlay"
