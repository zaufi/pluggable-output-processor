Changes
=======

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


Version [0.20]
--------------

* allow multiple parallel installations of the package. For example when
  one have a system-wide install and per user (into `~/.local`) maden via
  `pip install --editable=.` (or `./setup.py develop`).

Version [0.19]
--------------

* allow to put override symlinks to any location. The only requirement is
  that location must be the very first in `PATH`.

Version [0.18]
--------------

* fix exception in `cmake` processor when latter called from `make` process
* since the recent KDE Frameworks 5 release, there was a strange bug, when moving
  cursor above to 1 line act like moving on 2 lines instead. It looks like
  somewhere lines count has moved to zero base or smth like this...

Version [0.17]
--------------

* add `-l` option to list available modules

Version 0.16
------------

* break cycle dependency of `setup.py` on `termcolor` package (close #9)
* fix install instructions, upload to PyPi (close #10)

Version 0.14
------------

* few improvements in gcc colorizer
* user may have his own configs in `~/.outproc/` to override system-wide
  settings from `/etc/outproc/`
* support for true (16M) color terminals has been added! Now it is possible to
  specify `rgb(R,G,B)`, where components are numbers `0 <= N <= 255`.
  If all components are less than `6`, then `rgb` treated as (old) 256 color
  palette. Tested and work fine with KDE `konsole`.


Version 0.10
------------

* `diff` module added (capable to handle unified mode only nowadays)
* improve `gcc` module: handle `--help=<smth>` commands (w/ `-Q` as well) +
  few internal enhacements


Version 0.9
-----------

* make version info PEP 396 compliant
* little improvements in modules: `gcc`, `cmake`, `make`


Version 0.8
-----------

* few improvements in `gcc` module
* `make` module now can use `cmake` if found that latter running as its child
* fix a 'crash' in `make`

[Unreleased]: https://github.com/zaufi/pluggable-output-processor/compare/version-0.20...HEAD
[0.20]: https://github.com/zaufi/pluggable-output-processor/compare/version-0.19...version-0.20
[0.19]: https://github.com/zaufi/pluggable-output-processor/compare/version-0.18...version-0.19
[0.18]: https://github.com/zaufi/pluggable-output-processor/compare/version-0.17...version-0.18
[0.17]: https://github.com/zaufi/pluggable-output-processor/compare/version-0.16...version-0.17
