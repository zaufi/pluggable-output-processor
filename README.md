What is This?
=============

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

    $ tar -xzf outproc-X.Y.tar.gz
    $ cd outproc-X.Y
    $ sudo easy_install .

For Gentoo users there is a [live ebuild][raw-ebuild] in my [repository][my-overlay]. 
Also (for Gentoo users again ;-) `eselect` module from `contrib/` will be installed by the ebuild. 
Users of other distros have to make a symlinks to required modules manually:

    $ ln -s /usr/bin/outproc /usr/lib/outproc/bin/<module-name>

and then make sure `/usr/lib/outproc/bin` placed __before__ `/usr/bin` (and anything else) in your 
user/system `PATH` environment. Available modules (plugins) can be found at `<python-site-packages-dir>/outproc/pp`.
For example, to install the `gcc` module do the following:

    $ ln -s /usr/bin/outproc /usr/lib/outproc/bin/gcc

Then you may edit `/etc/outproc/gcc.conf` to adjust color settings. 


TODO
====

- [ ] continue to improve C++ tokenizer (few things can be better)
- [ ] unit tests for tokenizer
- [ ] test files w/ to cause various error messages from gcc (+ unit test for colorizer somehow)
- [ ] continue to improve `cmake` support (+ unit tests)
- [x] turn `mount` output into a human readable look-n-feel
- [ ] colorize `df` depending on free space threshold
- [ ] colorize `diff` (easy! :-) -- Done for `-u` mode
- [x] `eselect` module to manage tools under control
- [ ] ask module is it want to handle a current command or we can do `execv` instead
- [ ] implement `STDIN` reader (pipe mode)
- [ ] handle `KeyboardInterrupt` and hide Python crap
- [ ] `ctest` module to colorize test results
- [ ] handle as note:

        /usr/include/python3.3/pyconfig.h:1397:0: warning: "_XOPEN_SOURCE" redefined [enabled by default]
        #define _XOPEN_SOURCE 700
        <command-line>:0:0: note: this is the location of the previous definition
- [x] handle `make[1]: warning:`
- [x] handle `gcc -Q --help=<smth>`
- [x] support for TrueColor terminals (`konsole` for example)

See also
========

[raw-ebuld]: https://github.com/zaufi/zaufi-overlay/blob/master/dev-util/pluggable-output-processor/pluggable-output-processor-scm.ebuild
[my-overlay]: https://github.com/zaufi/zaufi-overlay/ "My ebuilds overlay"

[![Downloads](https://pypip.in/d/outproc/badge.png)](https://pypi.python.org/pypi/outproc)
[![Downloads](https://pypip.in/v/outproc/badge.png)](https://pypi.python.org/pypi/outproc)
[![Build Status](https://api.travis-ci.org/zaufi/pluggable-output-processor.png?branch=master)](https://travis-ci.org/zaufi/pluggable-output-processor)
[![Requirements Status](https://requires.io/github/zaufi/pluggable-output-processor/requirements.png?branch=master)](https://requires.io/github/zaufi/pluggable-output-processor/requirements/?branch=master)
