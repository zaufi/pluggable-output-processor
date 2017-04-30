Changes
=======

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
