What is This?
=============

Motivation
----------

_Pluggable Output Processor_ is my attempt to get rid of a bunch of various colorizers
from my system (like `colorgcc`, `colordiff`, `colorsvn`, ...) <del>and take everything under control</del>.
Some of them are written on Perl (and I'm not a fun of it :-) and after few hacks I've made to improve
`colorgcc`, I realized that I don't want to <del>waste my time</del> learn Perl.


Yes, I know there is a lot stuff like this, but I'm not a Perl programmer to improve them...
but have a lot of thoughts/ideas how to do that. The others are <del>too much</del>  _end-user oriented_ 
<del>so inflexible</del> -- they can colorize almost everything via configuration files and regular expressions. 
The only problem I have w/ them:
some of what I'd like to colorize is **damn hard to express via regexes** ... particularly because
line-by-line processing implemented in that tools have no _state_...


Features
--------

* easy (to Python programmers ;-) to extend
* 256 color terminal support ;-) configuration files in addition to standard named colors
  may contain color definitions as `rgb(r,g,b)` or `gray(n)`
* colorizers for `make`, `cmake`, `gcc` out of the box (more to come ;-)
* some modules are not just a stupid colorizers ;-) For example `gcc` can reformat text for
  better readability (really helps to understand template errors). Also `cmake` module can reduce
  amount of lines printed during test by collapsing test _intro_ message and _result_ into a single one.

// TBD


Installation
------------

Easy!

    $ tar -xzf outproc-X.Y.tar.gz
    $ cd outproc-X.Y
    $ sudo easy_install .

For Gentoo users there is a live ebuild in my repository. Also (for Gentoo users again ;-) eselect 
module from `contrib/` will be installed by the ebuild. Users of other distros have to make a symlinks 
to required modules manually:

    $ ln -s /usr/bin/outproc /usr/lib/outproc/bin/<module-name>

and then make sure `/usr/lib/outproc/bin` placed __before__ `/usr/bin` (and anything else) in your 
user/system `PATH` environment.


TODO
====

* continue to improve C++ tokenizer (few things can be better)
* unit tests for tokenizer
* test files w/ to cause various error messages from gcc (+ unit test for colorizer somehow)
* continue to improve `cmake` support (+ unit tests)
* turn `mount` output into a jumab readable look-n-feel
* colorize `df` depending on free space threshold
* colorize `diff` (easy! :-)
* `eselect` module to manage tools under control
* ask module is it want to handle a current command or we can do `execv` instead
* implement `STDIN` reader (pipe mode)
