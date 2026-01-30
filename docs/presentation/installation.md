# Installation

## Stable release

To install Optimal Cruise Computation, run this command in your terminal:

```console
$ pip install opti-cruise
```

This is the preferred method to install Optimal Cruise Computation, as it will always install the most recent stable release.

If you don't have [pip] installed, this [Python installation guide] can guide
you through the process.

````{note}
If you want to use Optimal Cruise Computation as a dependency in a UV-managed project, add it with
```console
$ uv add opti-cruise
```
````

## From sources

The sources for Optimal Cruise Computation can be downloaded from the [Github repo].

You can either clone the public repository:

```console
$ git clone git://github.com/balouf/opti-cruise
```

Or download the [tarball]:

```console
$ curl -OJL https://github.com/balouf/opti-cruise/tarball/main
```

Once you have a copy of the source, you can install it from the package directory with:

```console
$ pip install .
```

[github repo]: https://github.com/balouf/opti-cruise
[pip]: https://pip.pypa.io
[python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/
[tarball]: https://github.com/balouf/opti-cruise/tarball/main
