passagemath: General purpose mathematical software system, a fork of SageMath
=============================================================================

passagemath is open source mathematical software released under the GNU General Public
Licence GPLv2+.

It is a fork of [SageMath](https://www.sagemath.org/), created in October 2024 with the following goals:

* providing [modularized installation with pip](https://github.com/sagemath/sage/issues/29705),
* establishing first-class membership in the scientific Python ecosystem,
* giving [clear attribution of upstream projects](https://groups.google.com/g/sage-devel/c/6HO1HEtL1Fs/m/G002rPGpAAAJ),
* inviting collaborations with upstream projects,
* [maintaining a professional, respectful, inclusive community](https://groups.google.com/g/sage-devel/c/xBzaINHWwUQ),
* developing a port to [Pyodide](https://pyodide.org/en/stable/) for serverless deployment with Javascript,
* developing a native Windows port.

[People all around the globe](https://www.sagemath.org/development-map.html) have contributed to the
development of SageMath, and hence of passagemath.

[Full documentation](https://doc.sagemath.org/html/en/index.html) is available online.


passagemath community
---------------------

Join [passagemath.discourse.group](https://passagemath.discourse.group/) for help and discussions.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how you can contribute.


Full installation
-----------------

Unless you need to install passagemath into a specific existing environment, we recommend
to create and activate a fresh virtual environment over a suitable Python (3.9.x-3.12.x),
for example `~/passagemath-venv/`:

            $ python3 --version
            Python 3.12.7
            $ python3 -m venv ~/passagemath-venv
            $ source ~/passagemath-venv/bin/activate

Next, if you want to build from PyPI, use the following command:

            passagemath $ export SAGE_CONF_TARGETS=build

If you want to build from a local clone of the passagemath repository instead,
use the following command first.

            passagemath $ export SAGE_ROOT=$(pwd)
            passagemath $ export PIP_CONSTRAINT="$(pwd)/constraints_pkgs.txt"
            passagemath $ export SAGE_CONF_TARGETS=build-local

As the first installation step, install [![PyPI: passagemath-conf](https://img.shields.io/pypi/v/passagemath-conf.svg?label=passagemath-conf)](https://pypi.python.org/pypi/passagemath-conf),
which builds various prerequisite non-Python packages in a subdirectory of `~/.sage/`.
The build can be customized by setting `SAGE_CONF_CONFIGURE_ARGS`.

            (passagemath-venv) $ python3 -m pip install -v passagemath-conf

After a successful installation, a wheelhouse provides various Python packages.
You can list the wheels using the command:

            (passagemath-venv) $ ls $(sage-config SAGE_SPKG_WHEELS)

If this gives an error saying that `sage-config` is not found, check any messages
that the `pip install` command may have printed. You may need to adjust your `PATH`,
for example by:

            $ export PATH="$(python3 -c 'import sysconfig; print(sysconfig.get_path("scripts", "posix_user"))'):$PATH"

Now install the packages from the wheelhouse:

            (passagemath-venv) $ python3 -m pip install $(sage-config SAGE_SPKG_WHEELS)/*.whl

Next, install the [![PyPI: passagemath-setup](https://img.shields.io/pypi/v/passagemath-setup.svg?label=passagemath-setup)](https://pypi.python.org/pypi/passagemath-setup) package:

            (passagemath-venv) $ python3 -m pip install passagemath-setup

Finally, install the Sage library from the package [![PyPI: passagemath-standard](https://img.shields.io/pypi/v/passagemath-standard.svg?label=passagemath-standard)](https://pypi.python.org/pypi/passagemath-standard):

            (passagemath-venv) $ python3 -m pip install --no-build-isolation -v passagemath-standard

The above instructions install the latest stable release of passagemath.
To install the latest development version instead, add the switch `--pre` to all invocations of
`python3 -m pip install`.

Modularized distributions
-------------------------

passagemath provides the Sage library in a number of distributions (pip-installable packages) that can be installed separately.

Authors of packages that depend on the Sage library can declare dependencies on these distributions. The benefit for users of the package: There is no longer a need to first install Sage. Instead, the parts of the Sage library that are needed by the package are automatically installed. Thus, the package becomes a first-class member of the Python ecosystem.

- [sage-numerical-interactive-mip](https://github.com/passagemath/sage-numerical-interactive-mip) is an example of a pure Python package that [declares dependencies](https://github.com/passagemath/sage-numerical-interactive-mip/blob/master/pyproject.toml) on four distributions: passagemath-polyhedra, passagemath-plot, passagemath-repl, and passagemath-flint.
- [kerrgeodesic_gw](https://github.com/BlackHolePerturbationToolkit/kerrgeodesic_gw) is an example of a pure Python package that [declares optional dependencies ("extras-require")](https://github.com/BlackHolePerturbationToolkit/kerrgeodesic_gw/blob/master/setup.py#L49) on three distributions: passagemath-symbolics, passagemath-plot, and passagemath-repl.

Here is an overview of the available distribution packages.

### Distributions named after a basic mathematical structure

The packages may also cover a wide range of generalizations/applications of the structure after which they are named. Users who work in a specialized research area will, of course, recognize what structures they need. The down-to-earth naming also creates discoverability by a broader audience.

[![PyPI: passagemath-combinat](https://img.shields.io/pypi/v/passagemath-combinat.svg?label=passagemath-combinat)](https://pypi.python.org/pypi/passagemath-combinat) provides "everything combinatorial", except for graphs. It consists of about 350 first-party Python and Cython modules and also provides the functionality of [SYMMETRICA](http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA), the library for representation theory of the symmetric group, combinatorics of tableaux, symmetric functions, etc.

[![PyPI: passagemath-graphs](https://img.shields.io/pypi/v/passagemath-graphs.svg?label=passagemath-graphs)](https://pypi.python.org/pypi/passagemath-graphs) provides directed and undirected graphs, but also posets, combinatorial designs, abstract simplicial complexes, quivers, etc.  It consists of over 170 first-party Python and Cython modules and uses the [Boost Graph Library](https://github.com/boostorg/graph), with additional functionality from [NetworkX](https://networkx.github.io/) and several other libraries.

[![PyPI: passagemath-groups](https://img.shields.io/pypi/v/passagemath-groups.svg?label=passagemath-groups)](https://pypi.python.org/pypi/passagemath-groups) provides groups and invariant theory. It heavily depends on [GAP](https://www.gap-system.org) via passagemath-gap.

[![PyPI: passagemath-modules](https://img.shields.io/pypi/v/passagemath-modules.svg?label=passagemath-modules)](https://pypi.python.org/pypi/passagemath-modules) provides vector spaces, modules, matrices, tensors, homology, coding theory, abelian groups, matroids, etc. It consists of over 440 first-party Python and Cython modules and depends on the [GNU Scientific Library](http://www.gnu.org/software/gsl/) and [NumPy](https://numpy.org/).

[![PyPI: passagemath-polyhedra](https://img.shields.io/pypi/v/passagemath-polyhedra.svg?label=passagemath-polyhedra)](https://pypi.python.org/pypi/passagemath-polyhedra) provides convex polyhedra in arbitrary dimension on the basis of the [Parma Polyhedra Library](https://www.bugseng.com/ppl). It consists of about 130 first-party Python and Cython modules that also provide fans, hyperplane arrangements, polyhedral complexes, linear and mixed-integer optimization, lattice point sets, and toric varieties.

[![PyPI: passagemath-schemes](https://img.shields.io/pypi/v/passagemath-schemes.svg?label=passagemath-schemes)](https://pypi.python.org/pypi/passagemath-schemes) provides algebraic varieties, schemes, elliptic curves, modular forms, etc.

[![PyPI: passagemath-symbolics](https://img.shields.io/pypi/v/passagemath-symbolics.svg?label=passagemath-symbolics)](https://pypi.python.org/pypi/passagemath-symbolics) provides symbolic expressions implemented in Pynac, a fork of [GiNaC](https://www.ginac.de/), symbolic calculus using [Maxima](http://maxima.sourceforge.net), and interfaces to various other symbolic software systems including [SymPy](https://www.sympy.org/en/index.html), as well as differential geometry ([SageManifolds](https://sagemanifolds.obspm.fr/)).

### Distributions named after a third-party non-Python dependency

This makes technical sense because the dependencies will be localized to this distribution package, but it also helps give **attribution and visibility** to these libraries and projects that Sage depends on.
   | Standard packages | Optional packages  |
   | :---------------- | :----------------  |
   | [![PyPI: passagemath-cddlib](https://img.shields.io/pypi/v/passagemath-cddlib.svg?label=passagemath-cddlib)](https://pypi.python.org/pypi/passagemath-cddlib) provides the functionality of [cddlib](https://github.com/cddlib/cddlib), the library for polyhedral representation conversion. | [![PyPI: passagemath-benzene](https://img.shields.io/pypi/v/passagemath-benzene.svg?label=passagemath-benzene)](https://pypi.python.org/pypi/passagemath-benzene)  |
   | [![PyPI: passagemath-cliquer](https://img.shields.io/pypi/v/passagemath-cliquer.svg?label=passagemath-cliquer)](https://pypi.python.org/pypi/passagemath-cliquer) provides the functionality of [cliquer](https://users.aalto.fi/~pat/cliquer.html), finding cliques in weighted graphs. | [![PyPI: passagemath-bliss](https://img.shields.io/pypi/v/passagemath-bliss.svg?label=passagemath-bliss)](https://pypi.python.org/pypi/passagemath-bliss) provides the functionality of [bliss](https://users.aalto.fi/~tjunttil/bliss/index.html), a tool for computing automorphism groups and canonical forms of graphs.  |
   | [![PyPI: passagemath-eclib](https://img.shields.io/pypi/v/passagemath-eclib.svg?label=passagemath-eclib)](https://pypi.python.org/pypi/passagemath-eclib) provides modules depending on [eclib](https://github.com/JohnCremona/eclib), the library for enumerating and computing with elliptic curves defined over the rational numbers. |   |
   | [![PyPI: passagemath-flint](https://img.shields.io/pypi/v/passagemath-flint.svg?label=passagemath-flint)](https://pypi.python.org/pypi/passagemath-flint) provides modules depending on [FLINT](https://flintlib.org), the Fast Library for Number Theory. | [![PyPI: passagemath-brial](https://img.shields.io/pypi/v/passagemath-brial.svg?label=passagemath-brial)](https://pypi.python.org/pypi/passagemath-brial) provides the functionality of [BRiAl](https://github.com/BRiAl/BRiAl), a Boolean Ring Algebra implementation using binary decision diagrams, the successor to PolyBoRi.  |
   | [![PyPI: passagemath-gap](https://img.shields.io/pypi/v/passagemath-gap.svg?label=passagemath-gap)](https://pypi.python.org/pypi/passagemath-gap) provides modules depending on [GAP](https://www.gap-system.org), the system for computational discrete algebra with particular emphasis on Computational Group Theory. | [![PyPI: passagemath-buckygen](https://img.shields.io/pypi/v/passagemath-buckygen.svg?label=passagemath-buckygen)](https://pypi.python.org/pypi/passagemath-buckygen)  |
   | [![PyPI: passagemath-gfan](https://img.shields.io/pypi/v/passagemath-gfan.svg?label=passagemath-gfan)](https://pypi.python.org/pypi/passagemath-gfan) provides the functionality of [gfan](https://users-math.au.dk/jensen/software/gfan/gfan.html), computing Groebner fans and tropical varieties. | [![PyPI: passagemath-coxeter3](https://img.shields.io/pypi/v/passagemath-coxeter3.svg?label=passagemath-coxeter3)](https://pypi.python.org/pypi/passagemath-coxeter3)  |
   | [![PyPI: passagemath-giac](https://img.shields.io/pypi/v/passagemath-giac.svg?label=passagemath-giac)](https://pypi.python.org/pypi/passagemath-giac) provides the functionality of [Giac](http://www-fourier.ujf-grenoble.fr/~parisse/giac.html), a general purpose computer algebra system. | [![PyPI: passagemath-frobby](https://img.shields.io/pypi/v/passagemath-frobby.svg?label=passagemath-frobby)](https://pypi.python.org/pypi/passagemath-frobby)  |
   | [![PyPI: passagemath-glpk](https://img.shields.io/pypi/v/passagemath-glpk.svg?label=passagemath-glpk)](https://pypi.python.org/pypi/passagemath-glpk) provides a mixed integer linear optimization backend using [GLPK](http://www.gnu.org/software/glpk), the GNU Linear Programming Kit. | [![PyPI: passagemath-glucose](https://img.shields.io/pypi/v/passagemath-glucose.svg?label=passagemath-glucose)](https://pypi.python.org/pypi/passagemath-glucose)  |
   | [![PyPI: passagemath-homfly](https://img.shields.io/pypi/v/passagemath-homfly.svg?label=passagemath-homfly)](https://pypi.python.org/pypi/passagemath-homfly) provides the functionality of [libhomfly](https://github.com/miguelmarco/libhomfly), the library to compute the homfly polynomial of knots and links. | [![PyPI: passagemath-kissat](https://img.shields.io/pypi/v/passagemath-kissat.svg?label=passagemath-kissat)](https://pypi.python.org/pypi/passagemath-kissat)  |
   | [![PyPI: passagemath-lcalc](https://img.shields.io/pypi/v/passagemath-lcalc.svg?label=passagemath-lcalc)](https://pypi.python.org/pypi/passagemath-lcalc) provides the functionality of [lcalc](http://oto.math.uwaterloo.ca/~mrubinst/L_function_public/L.html), the L-function calculator. | [![PyPI: passagemath-latte-4ti2](https://img.shields.io/pypi/v/passagemath-latte-4ti2.svg?label=passagemath-latte-4ti2)](https://pypi.python.org/pypi/passagemath-latte-4ti2) provides  interfaces to [LattE integrale](https://www.math.ucdavis.edu/~latte/) and [4ti2](https://github.com/4ti2/4ti2)  |
   | [![PyPI: passagemath-libbraiding](https://img.shields.io/pypi/v/passagemath-libbraiding.svg?label=passagemath-libbraiding)](https://pypi.python.org/pypi/passagemath-libbraiding) provides the functionality of [libbraiding](https://github.com/miguelmarco/libbraiding), computing centralizers, conjugacy, and other properties of braids. | [![PyPI: passagemath-lrslib](https://img.shields.io/pypi/v/passagemath-lrslib.svg?label=passagemath-lrslib)](https://pypi.python.org/pypi/passagemath-lrslib) provides the functionality of [lrslib](http://cgm.cs.mcgill.ca/~avis/C/lrs.html), reverse search for vertex enumeration and convex hull problems. |
   | [![PyPI: passagemath-libecm](https://img.shields.io/pypi/v/passagemath-libecm.svg?label=passagemath-libecm)](https://pypi.python.org/pypi/passagemath-libecm) provides the functionality of [GMP-ECM](https://gitlab.inria.fr/zimmerma/ecm), the elliptic curve method for integer factorization. | [![PyPI: passagemath-macaulay2](https://img.shields.io/pypi/v/passagemath-macaulay2.svg?label=passagemath-macaulay2)](https://pypi.python.org/pypi/passagemath-macaulay2)  |
   | [![PyPI: passagemath-linbox](https://img.shields.io/pypi/v/passagemath-linbox.svg?label=passagemath-linbox)](https://pypi.python.org/pypi/passagemath-linbox) | [![PyPI: passagemath-mcqd](https://img.shields.io/pypi/v/passagemath-mcqd.svg?label=passagemath-mcqd)](https://pypi.python.org/pypi/passagemath-mcqd)  |
   | [![PyPI: passagemath-nauty](https://img.shields.io/pypi/v/passagemath-nauty.svg?label=passagemath-nauty)](https://pypi.python.org/pypi/passagemath-nauty) provides the functionality of [nauty and traces](https://pallini.di.uniroma1.it), computing automorphism groups of graphs and digraphs. | [![PyPI: passagemath-meataxe](https://img.shields.io/pypi/v/passagemath-meataxe.svg?label=passagemath-meataxe)](https://pypi.python.org/pypi/passagemath-meataxe)  |
   | [![PyPI: passagemath-ntl](https://img.shields.io/pypi/v/passagemath-ntl.svg?label=passagemath-ntl)](https://pypi.python.org/pypi/passagemath-ntl) provides the functionality of [NTL](http://www.shoup.net/ntl/), a library for doing number theory. | [![PyPI: passagemath-msolve](https://img.shields.io/pypi/v/passagemath-msolve.svg?label=passagemath-msolve)](https://pypi.python.org/pypi/passagemath-msolve) provides an interface to [msolve](https://msolve.lip6.fr/), the polynomial system solver.  |
   | [![PyPI: passagemath-palp](https://img.shields.io/pypi/v/passagemath-palp.svg?label=passagemath-palp)](https://pypi.python.org/pypi/passagemath-palp) provides the functionality of [PALP](http://hep.itp.tuwien.ac.at/~kreuzer/CY/CYpalp.html), lattice polytopes with applications to toric geometry. | [![PyPI: passagemath-plantri](https://img.shields.io/pypi/v/passagemath-plantri.svg?label=passagemath-plantri)](https://pypi.python.org/pypi/passagemath-plantri) provides the functionality of [plantri](https://users.cecs.anu.edu.au/~bdm/plantri/), generating planar graphs. |
   | [![PyPI: passagemath-pari](https://img.shields.io/pypi/v/passagemath-pari.svg?label=passagemath-pari)](https://pypi.python.org/pypi/passagemath-pari) provides the functionality of [PARI/GP](http://pari.math.u-bordeaux.fr/), the computer algebra system for fast computations in number theory. | [![PyPI: passagemath-qepcad](https://img.shields.io/pypi/v/passagemath-qepcad.svg?label=passagemath-qepcad)](https://pypi.python.org/pypi/passagemath-qepcad) provides the functionality of [QEPCAD](https://github.com/chriswestbrown/qepcad), quantifier elimination by partial cylindrical algebraic decomposition.  |
   | [![PyPI: passagemath-planarity](https://img.shields.io/pypi/v/passagemath-planarity.svg?label=passagemath-planarity)](https://pypi.python.org/pypi/passagemath-planarity) provides the functionality of the [Edge Addition Planarity Suite](https://github.com/graph-algorithms/edge-addition-planarity-suite/) for graphs. | [![PyPI: passagemath-rubiks](https://img.shields.io/pypi/v/passagemath-rubiks.svg?label=passagemath-rubiks)](https://pypi.python.org/pypi/passagemath-rubiks) provides algorithms for Rubik's cube.  |
   | [![PyPI: passagemath-rankwidth](https://img.shields.io/pypi/v/passagemath-rankwidth.svg?label=passagemath-rankwidth)](https://pypi.python.org/pypi/passagemath-rankwidth) provides the functionality of [rw](https://sourceforge.net/projects/rankwidth), rank decompositions of graphs. | [![PyPI: passagemath-sirocco](https://img.shields.io/pypi/v/passagemath-sirocco.svg?label=passagemath-sirocco)](https://pypi.python.org/pypi/passagemath-sirocco) provides the functinality of [sirocco](https://github.com/miguelmarco/SIROCCO2), certified root continuation of bivariate polynomials. |
   | [![PyPI: passagemath-singular](https://img.shields.io/pypi/v/passagemath-singular.svg?label=passagemath-singular)](https://pypi.python.org/pypi/passagemath-singular) provides the functionality from [Singular](https://www.singular.uni-kl.de/), the computer algebra system for polynomial computations, algebraic geometry, singularity theory. | [![PyPI: passagemath-tdlib](https://img.shields.io/pypi/v/passagemath-tdlib.svg?label=passagemath-tdlib)](https://pypi.python.org/pypi/passagemath-tdlib) provides the functionality of [treedec](https://gitlab.com/freetdi/treedec), algorithms concerning tree decompositions of graphs.  |
   | [![PyPI: passagemath-sympow](https://img.shields.io/pypi/v/passagemath-sympow.svg?label=passagemath-sympow)](https://pypi.python.org/pypi/passagemath-sympow) provides the functionality of [sympow](https://gitlab.com/rezozer/forks/sympow), special values of symmetric power elliptic curve L-functions.  | [![PyPI: passagemath-topcom](https://img.shields.io/pypi/v/passagemath-topcom.svg?label=passagemath-topcom)](https://pypi.python.org/pypi/passagemath-topcom) provides the functionality of [TOPCOM](https://www.wm.uni-bayreuth.de/de/team/rambau_joerg/TOPCOM/), triangulations of point configurations and oriented matroids.  |

### Distributions named after a technical functionality

[![PyPI: passagemath-objects](https://img.shields.io/pypi/v/passagemath-objects.svg?label=passagemath-objects)](https://pypi.python.org/pypi/passagemath-objects) Sage extends Python's object system by dynamic   mix-in classes that are driven by categories and axioms. It is loosely   modeled on concepts of category theory and inspired by   Scratchpad/Axiom/FriCAS, Magma, and MuPAD. This distribution package makes Sage objects, the element/parent framework, basic categories and functors,   the coercion system and the related metaclasses available. It only depends on the basic arithmetic libraries [GMP](http://gmplib.org), [MPFR](http://mpfr.org/), [MPC](https://www.multiprecision.org/mpc), on the Cython interface [gmpy2](https://pypi.org/project/gmpy2/) to these libraries, and on  [cysignals](https://github.com/sagemath/cysignals).

[![PyPI: passagemath-categories](https://img.shields.io/pypi/v/passagemath-categories.svg?label=passagemath-categories)](https://pypi.python.org/pypi/passagemath-categories) This distribution package contains the full set of categories defined by Sage, as well as basic mathematical objects such as integers and rational numbers, a basic implementation of polynomials, and affine spaces.  None of this brings in additional dependencies.

[![PyPI: passagemath-environment](https://img.shields.io/pypi/v/passagemath-environment.svg?label=passagemath-environment)](https://pypi.python.org/pypi/passagemath-environment) provides the `sage` script for launching the Sage REPL and accessing various developer tools and Python modules that provide the connection to the system and software environment.

[![PyPI: passagemath-repl](https://img.shields.io/pypi/v/passagemath-repl.svg?label=passagemath-repl)](https://pypi.python.org/pypi/passagemath-repl) The top-level interactive environment with the preparser that defines the surface language of Sage. This distribution also includes the doctesting facilities (`sage -t`), as the doctests are written in the surface language.

[![PyPI: passagemath-plot](https://img.shields.io/pypi/v/passagemath-plot.svg?label=passagemath-plot)](https://pypi.python.org/pypi/passagemath-plot) Plotting facilities, depending on [matplotlib](https://matplotlib.org).

[![PyPI: passagemath-standard-no-symbolics](https://img.shields.io/pypi/v/passagemath-standard-no-symbolics.svg?label=passagemath-standard-no-symbolics)](https://pypi.python.org/pypi/passagemath-standard-no-symbolics) Ideally an empty meta-package that depends on everything that is not in passagemath-symbolics; as a catch-all mechanism, this distribution ships all modules that do not carry a `# sage_setup: distribution = ...` directive.

[![PyPI: passagemath-standard](https://img.shields.io/pypi/v/passagemath-standard.svg?label=passagemath-standard)](https://pypi.python.org/pypi/passagemath-standard) Everything as provided by a standard installation of the Sage distribution. This is reduced to an empty meta-package.

[![PyPI: passagemath-conf](https://img.shields.io/pypi/v/passagemath-conf.svg?label=passagemath-conf)](https://pypi.python.org/pypi/passagemath-conf) Confectionery and configuration system.

[![PyPI: passagemath-setup](https://img.shields.io/pypi/v/passagemath-setup.svg?label=passagemath-setup)](https://pypi.python.org/pypi/passagemath-setup) Build system for the Sage library.

[![PyPI: passagemath-docbuild](https://img.shields.io/pypi/v/passagemath-docbuild.svg?label=passagemath-docbuild)](https://pypi.python.org/pypi/passagemath-docbuild) Build system for the Sage documentation.



Table of Contents
-----------------

* [Getting Started](#getting-started)
* [Supported Platforms](#supported-platforms)
* [\[Windows\] Preparing the Platform](#windows-preparing-the-platform)
* [\[macOS\] Preparing the Platform](#macos-preparing-the-platform)
* [Instructions to Build from Source](#instructions-to-build-from-source)
* [SageMath Docker Images](#sagemath-docker-images)
* [Directory Layout](#directory-layout)
* [Build System](#build-system)
* [Relocation](#relocation)
* [Redistribution](#redistribution)
* [Build System](#build-system)
* [Changes to Included Software](#changes-to-included-software)

Getting Started
---------------

Those who are impatient may use prebuilt Sage available online from any of

<!-- [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sagemath/sage-binder-env/master
) &nbsp; --->
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/passagemath/passagemath/tree/main
) &nbsp; [![Open in GitHub Codespaces](https://img.shields.io/badge/Open_in_GitHub_Codespaces-black?logo=github)](https://codespaces.new/passagemath/passagemath/tree/main)

without local installation. Otherwise read on.

The [Sage Installation Guide](https://doc.sagemath.org/html/en/installation/index.html)
provides a decision tree that guides you to the type of installation
that will work best for you. This includes building from source,
obtaining Sage from a package manager, using a container image, or using
Sage in the cloud.

**This README contains self-contained instructions for building Sage from source.**
This requires you to clone the git repository (as described in this README) or download the
[sources](https://www.sagemath.org/download-source.html) in the form
of a tarball.

Supported Platforms
-------------------

Sage attempts to support all major Linux distributions, recent versions of
macOS, and Windows (using Windows Subsystem for Linux or
virtualization).

Detailed information on supported platforms for a specific version of Sage
can be found in the section _Availability and installation help_ of the
[release notes for this version](https://github.com/passagemath/passagemath/releases).

We highly appreciate contributions to Sage that fix portability bugs
and help port Sage to new platforms; let us know at the [sage-devel
mailing list](https://groups.google.com/group/sage-devel).

[Windows] Preparing the Platform
--------------------------------

The preferred way to run Sage on Windows is using Windows Subsystem for
Linux (WSL). Follow the
[official WSL setup guide](https://docs.microsoft.com/en-us/windows/wsl/faq)
to install Ubuntu (or another Linux distribution).
Make sure you allocate WSL sufficient RAM; 5GB is known to work, while
2GB might be not enough for building Sage from source.
Then all instructions for installation in Linux apply.

As an alternative, you can also run Linux on Windows using Docker ([see
below](#sagemath-docker-images)) or other virtualization solutions.

[macOS] Preparing the Platform
------------------------------

- If your Mac uses the Apple Silicon (M1, M2, M3, M4; arm64) architecture and
  you set up your Mac by transferring files from an older Mac, make sure
  that the directory ``/usr/local`` does not contain an old copy of Homebrew
  (or other software) for the x86_64 architecture that you may have copied
  over.  Note that Homebrew for the M1 is installed in ``/opt/homebrew``, not
  ``/usr/local``.

- If you wish to use conda, please see the [section on
  conda](https://doc.sagemath.org/html/en/installation/conda.html) in the Sage
  Installation Manual for guidance.

- Otherwise, we strongly recommend to use Homebrew ("the missing package
  manager for macOS") from https://brew.sh/, which provides the ``gfortran``
  compiler and many libraries.

- Otherwise, if you do not wish to install Homebrew, you will need to install
  the latest version of Xcode Command Line Tools.  Open a terminal window and
  run `xcode-select --install`; then click "Install" in the pop-up window.  If
  the Xcode Command Line Tools are already installed, you may want to check if
  they need to be updated by typing `softwareupdate -l`.

Instructions to Build from Source
---------------------------------

Like many other software packages, Sage is built from source using
`./configure`, followed by `make`.  However, we strongly recommend to
read the following step-by-step instructions for building Sage.

The instructions cover all of Linux, macOS, and WSL.

More details, providing a background for these instructions, can be found
in the section [Install from Source Code](https://doc.sagemath.org/html/en/installation/source.html)
in the Installation Guide.


1.  Decide on the source/build directory (`SAGE_ROOT`):

    - On personal computers, any subdirectory of your :envvar:`HOME`
      directory should do.

    - For example, you could use `SAGE_ROOT=~/sage/sage`, which we
      will use as the running example below.

    - You need at least 10 GB of free disk space.

    - The full path to the source directory must contain **no spaces**.

    - After starting the build, you cannot move the source/build
      directory without breaking things.

    - You may want to avoid slow filesystems such as
      [network file systems (NFS)](https://en.wikipedia.org/wiki/Network_File_System)
      and the like.

    - [macOS] macOS allows changing directories without using exact capitalization.
      Beware of this convenience when compiling for macOS. Ignoring exact
      capitalization when changing into :envvar:`SAGE_ROOT` can lead to build
      errors for dependencies requiring exact capitalization in path names.

2.  Clone the sources with `git`:

    - To check that `git` is available, open a terminal and enter
      the following command at the shell prompt (`$`):

            $ git --version
            git version 2.42.0

      The exact version does not matter, but if this command gives an error,
      install `git` using your package manager, using one of these commands:

            $ sudo pacman -S git                          # on Arch Linux
            $ sudo apt-get update && apt-get install git  # on Debian/Ubuntu
            $ sudo yum install git                        # on Fedora/Redhat/CentOS
            $ sudo zypper install git                     # on openSUSE
            $ sudo xbps-install git                       # on Void Linux

    - Create the directory where `SAGE_ROOT` should be established:

            $ mkdir -p ~/sage
            $ cd ~/sage

    - Clone the passagemath git repository:

            $ git clone -c core.symlinks=true --filter blob:none  \
                        --origin passagemath \
                        https://github.com/passagemath/passagemath.git

      This will create the subdirectory `~/sage/passagemath`. (See the section
      [Setting up git](https://doc.sagemath.org/html/en/developer/git_setup.html)
      and the following sections in the Sage Developer's Guide
      for more information.)

    - Change into the created subdirectory:

            $ cd passagemath

    - [Windows] The Sage source tree contains symbolic links, and the
      build will not work if Windows line endings rather than UNIX
      line endings are used.

      Therefore it is recommended (but not necessary) to use the
      WSL version of `git`.

3.  Install system packages.

    Either refer for this to the [section on installation from
    source](https://doc.sagemath.org/html/en/installation/source.html) in the
    Sage Installation Manual for compilations of system packages
    that you can install. When done, skip to step 7 (bootstrapping).

    Alternatively, follow the more fine-grained approach below.

4.  [Linux, WSL] Install the required minimal build prerequisites:

    - Compilers: `gcc`, `gfortran`, `g++` (GCC versions from 9.x to 14.x
      and recent versions of Clang (LLVM) are supported).
      See [build/pkgs/gcc/SPKG.rst](build/pkgs/gcc/SPKG.rst) and
      [build/pkgs/gfortran/SPKG.rst](build/pkgs/gfortran/SPKG.rst)
      for a discussion of suitable compilers.

    - Build tools: GNU `make`, GNU `m4`, `perl` (including
      `ExtUtils::MakeMaker`), `ranlib`, `git`, `tar`, `bc`.
      See [build/pkgs/_prereq/SPKG.rst](build/pkgs/_prereq/SPKG.rst) for
      more details.

    - Python 3.4 or later, or Python 2.7, a full installation including
      `urllib`; but ideally version 3.9.x, 3.10.x, 3.11.x, 3.12.x, which
      will avoid having to build Sage's own copy of Python 3.
      See [build/pkgs/python3/SPKG.rst](build/pkgs/python3/SPKG.rst)
      for more details.

    We have collected lists of system packages that provide these build
    prerequisites. See, in the folder
    [build/pkgs/_prereq/distros](build/pkgs/_prereq/distros),
    the files
    [arch.txt](build/pkgs/_prereq/distros/arch.txt),
    [debian.txt](build/pkgs/_prereq/distros/debian.txt)
    (also for Ubuntu, Linux Mint, etc.),
    [fedora.txt](build/pkgs/_prereq/distros/fedora.txt)
    (also for Red Hat, CentOS),
    [opensuse.txt](build/pkgs/_prereq/distros/opensuse.txt),
    [slackware.txt](build/pkgs/_prereq/distros/slackware.txt), and
    [void.txt](build/pkgs/_prereq/distros/void.txt), or visit
    https://doc.sagemath.org/html/en/reference/spkg/_prereq.html#spkg-prereq

5.  Optional: It is recommended that you have both LaTeX and
    the ImageMagick tools (e.g. the "convert" command) installed
    since some plotting functionality benefits from them.

6.  [Development] If you plan to do Sage development or otherwise work with
    ticket branches and not only releases, install the bootstrapping
    prerequisites. See the files in the folder
    [build/pkgs/_bootstrap/distros](build/pkgs/_bootstrap/distros), or
    visit
    https://doc.sagemath.org/html/en/reference/spkg/_bootstrap.html#spkg-bootstrap

7.  Bootstrap the source tree using the following command:

        $ make configure

    (If the bootstrapping prerequisites are not installed, this command
    will download a package providing pre-built bootstrap output instead.)

8.  Sanitize the build environment. Use the command

        $ env

    to inspect the current environment variables, in particular `PATH`,
    `PKG_CONFIG_PATH`, `LD_LIBRARY_PATH`, `CFLAGS`, `CPPFLAGS`, `CXXFLAGS`,
    and `LDFLAGS` (if set).

    Remove items from these (colon-separated) environment variables
    that Sage should not use for its own build. In particular, remove
    items if they refer to a previous Sage installation.

    - [WSL] In particular, WSL imports many items from the Windows
      `PATH` variable into the Linux environment, which can lead to
      confusing build errors. These items typically start with `/mnt/c`.
      It is best to remove all of them from the environment variables.
      For example, you can set `PATH` using the command:

            $ export PATH=/usr/sbin/:/sbin/:/bin/:/usr/lib/wsl/lib/

    - [macOS with homebrew] Set required environment variables for the build:

            $ source ./.homebrew-build-env

      This is to make some of Homebrew's packages (so-called keg-only
      packages) available for the build. Run it once to apply the
      suggestions for the current terminal session. You may need to
      repeat this command before you rebuild Sage from a new terminal
      session, or after installing additional homebrew packages.  (You
      can also add it to your shell profile so that it gets run
      automatically in all future sessions.)

9.  Optionally, decide on the installation prefix (`SAGE_LOCAL`):

    - Traditionally, and by default, Sage is installed into the
      subdirectory hierarchy rooted at `SAGE_ROOT/local/`.

    - This can be changed using `./configure --prefix=SAGE_LOCAL`,
      where `SAGE_LOCAL` is the desired installation prefix, which
      must be writable by the user.

      Unless you use this option in combination with `--enable-editable`,
      you can delete the entire Sage source tree after completing
      the build process.  What is installed in `SAGE_LOCAL` will be
      a self-contained installation of Sage.

    - Note that in Sage's build process, `make` builds **and**
      installs (`make install` is a no-op).  Therefore the
      installation hierarchy must be writable by the user.

    - See the Sage Installation Manual for options if you want to
      install into shared locations such as `/usr/local/`.
      Do not attempt to build Sage as `root`.

10. Optionally, review the configuration options, which includes
    many optional packages:

        $ ./configure --help

    Notable options for Sage developers are the following:

    - Use the option `--config-cache` to have `configure`
      keep a disk cache of configuration values. This gives a nice speedup
      when trying out ticket branches that make package upgrades, which
      involves automatic re-runs of the configuration step.

    - Use the option `--enable-ccache` to have Sage install and use the
      optional package `ccache`, which is preconfigured to keep a
      disk cache of object files created from source files. This can give
      a great speedup when switching between different branches, at the
      expense of disk space use.

11. Optional, but highly recommended: Set some environment variables to
    customize the build.

    For example, the `MAKE` environment variable controls whether to
    run several jobs in parallel.  On a machine with 4 processors, say,
    typing `export MAKE="make -j4"` will configure the build script to
    perform a parallel compilation of Sage using 4 jobs. On some
    powerful machines, you might even consider `-j16`, as building with
    more jobs than CPU cores can speed things up further.

    To reduce the terminal output during the build, type `export V=0`.
    (`V` stands for "verbosity".)

    Some environment variables deserve a special mention: `CC`,
    `CXX` and `FC`. These variables defining your compilers
    can be set at configuration time and their values will be recorded for
    further use at build time and runtime.

    For an in-depth discussion of more environment variables for
    building Sage, see [the installation
    guide](https://doc.sagemath.org/html/en/installation/source.html#environment-variables).

12. Type `./configure`, followed by any options that you wish to use.
    For example, to build Sage with `gf2x` package supplied by Sage,
    use `./configure --with-system-gf2x=no`.

    At the end of a successful `./configure` run, you may see messages
    recommending to install extra system packages using your package
    manager.

    For a large [list of Sage
    packages](https://github.com/sagemath/sage/issues/27330), Sage is able to
    detect whether an installed system package is suitable for use with
    Sage; in that case, Sage will not build another copy from source.

    Sometimes, the messages will recommend to install packages that are
    already installed on your system. See the earlier configure
    messages or the file `config.log` for explanation.  Also, the
    messages may recommend to install packages that are actually not
    available; only the most recent releases of your distribution will
    have all of these recommended packages.

13. Optional: If you choose to install the additional system packages,
    a re-run of `./configure` will test whether the versions installed
    are usable for Sage; if they are, this will reduce the compilation
    time and disk space needed by Sage. The usage of packages may be
    adjusted by `./configure` parameters (check again the output of
    `./configure --help`).

14. Type `make`.  That's it! Everything is automatic and
    non-interactive.

    If you followed the above instructions, in particular regarding the
    installation of system packages recommended by the output of
    `./configure` (step 11), and regarding the parallel build (step 10),
    building Sage takes less than one hour on a modern computer.
    (Otherwise, it can take much longer.)

    The build should work fine on all fully supported platforms. If it
    does not, we want to know!

15. Type `./sage` to try it out. In Sage, try for example `2 + 2`,
    `plot(x^2)`, `plot3d(lambda x, y: x*y, (-1, 1), (-1, 1))`
    to test a simple computation and plotting in 2D and 3D.
    Type <kbd>Ctrl</kbd>+<kbd>D</kbd> or `quit` to quit Sage.

16. Optional: Type `make ptestlong` to test all examples in the documentation
    (over 200,000 lines of input!) -- this takes from 10 minutes to
    several hours. Don't get too disturbed if there are 2 to 3 failures,
    but always feel free to email the section of `logs/ptestlong.log` that
    contains errors to the [sage-support mailing list](https://groups.google.com/group/sage-support).
    If there are numerous failures, there was a serious problem with your build.

17. The HTML version of the [documentation](https://doc.sagemath.org/html/en/index.html)
    is built during the compilation process of Sage and resides in the directory
    `local/share/doc/sage/html/`. You may want to bookmark it in your browser.

18. Optional: If you want to build the PDF version of the documentation,
    run `make doc-pdf` (this requires LaTeX to be installed).

19. Optional: Install optional packages of interest to you:
    get a list by typing  `./sage --optional` or by visiting the
    [packages documentation page](https://doc.sagemath.org/html/en/reference/spkg/).

20. Optional: Create a symlink to the installed `sage` script in a
    directory in your `PATH`, for example `/usr/local`. This will
    allow you to start Sage by typing `sage` from anywhere rather than
    having to either type the full path or navigate to the Sage
    directory and type `./sage`. This can be done by running:

        $ sudo ln -s $(./sage -sh -c 'ls $SAGE_ROOT/venv/bin/sage') /usr/local/bin

21. Optional: Set up SageMath as a Jupyter kernel in an existing Jupyter notebook
    or JupyterLab installation, as described in the section
    [Launching SageMath](https://doc.sagemath.org/html/en/installation/launching.html)
    in the Sage Installation Guide.

Directory Layout
----------------

Simplified directory layout (only essential files/directories):
```
SAGE_ROOT                 Root directory (create by git clone)
├── build
│   └── pkgs              Every package is a subdirectory here
│       ├── 4ti2/
│       …
│       └── zlib/
├── configure             Top-level configure script
├── COPYING.txt           Copyright information
├── pkgs                  Source trees of Python distribution packages
│   ├── sage-conf
│   │   ├── sage_conf.py
│   │   └── setup.py
│   ├── sage-docbuild
│   │   ├── sage_docbuild/
│   │   └── setup.py
│   ├── sage-setup
│   │   ├── sage_setup/
│   │   └── setup.py
│   ├── sage-sws2rst
│   │   ├── sage_sws2rst/
│   │   └── setup.py
│   └── sagemath-standard
│       ├── bin/
│       ├── sage -> ../../src/sage
│       └── setup.py
├── local  (SAGE_LOCAL)   Installation hierarchy for non-Python packages
│   ├── bin               Executables
│   ├── include           C/C++ headers
│   ├── lib               Shared libraries, architecture-dependent data
│   ├── share             Databases, architecture-independent data, docs
│   │   └── doc           Viewable docs of Sage and of some components
│   └── var
│       ├── lib/sage
│       │   ├── installed/
│       │   │             Records of installed non-Python packages
│       │   ├── scripts/  Scripts for uninstalling installed packages
│       │   └── venv-python3.9  (SAGE_VENV)
│       │       │         Installation hierarchy (virtual environment)
│       │       │         for Python packages
│       │       ├── bin/  Executables and installed scripts
│       │       ├── lib/python3.9/site-packages/
│       │       │         Python modules/packages are installed here
│       │       └── var/lib/sage/
│       │           └── wheels/
│       │                 Python wheels for all installed Python packages
│       │
│       └── tmp/sage/     Temporary files when building Sage
├── logs
│   ├── install.log       Full install log
│   └── pkgs              Build logs of individual packages
│       ├── alabaster-0.7.12.log
│       …
│       └── zlib-1.2.11.log
├── m4                    M4 macros for generating the configure script
│   └── *.m4
├── Makefile              Running "make" uses this file
├── prefix -> SAGE_LOCAL  Convenience symlink to the installation tree
├── README.md             This file
├── sage                  Script to start Sage
├── src                   Monolithic Sage library source tree
│   ├── bin/              Scripts that Sage uses internally
│   ├── doc/              Sage documentation sources
│   └── sage/             The Sage library source code
├── upstream              Source tarballs of packages
│   ├── Babel-2.9.1.tar.gz
│   …
│   └── zlib-1.2.11.tar.gz
├── venv -> SAGE_VENV     Convenience symlink to the virtual environment
└── VERSION.txt
```
For more details see [our Developer's Guide](https://doc.sagemath.org/html/en/developer/coding_basics.html#files-and-directory-structure).

Build System
------------

This is a brief summary of the Sage software distribution's build system.
There are two components to the full Sage system--the Sage Python library
and its associated user interfaces, and the larger software distribution of
Sage's main dependencies (for those dependencies not supplied by the user's
system).

Sage's Python library is built and installed using a `setup.py` script as is
standard for Python packages (Sage's `setup.py` is non-trivial, but not
unusual).

Most of the rest of the build system is concerned with building all of Sage's
dependencies in the correct order in relation to each other.  The dependencies
included by Sage are referred to as SPKGs (i.e. "Sage Packages") and are listed
under `build/pkgs`.

The main entrypoint to Sage's build system is the top-level `Makefile` at the
root of the source tree.  Unlike most normal projects that use autoconf (Sage
does as well, as described below), this `Makefile` is not generated.  Instead,
it contains a few high-level targets and targets related to bootstrapping the
system.  Nonetheless, we still run `make <target>` from the root of the source
tree--targets not explicitly defined in the top-level `Makefile` are passed
through to another Makefile under `build/make/Makefile`.

The latter `build/make/Makefile` *is* generated by an autoconf-generated
`configure` script, using the template in `build/make/Makefile.in`.  This
includes rules for building the Sage library itself (`make sagelib`), and for
building and installing each of Sage's dependencies (e.g. `make gf2x`).

The `configure` script itself, if it is not already built, can be generated by
running the `bootstrap` script (the latter requires _GNU autotools_ being installed).
The top-level `Makefile` also takes care of this automatically.

To summarize, running a command like `make python3` at the top-level of the
source tree goes something like this:

1.  `make python3`
2.  run `./bootstrap` if `configure` needs updating
3.  run `./configure` with any previously configured options if `build/make/Makefile`
    needs updating
4.  change directory into `build/make` and run the `install` script--this is
    little more than a front-end to running `make -f build/make/Makefile python3`,
    which sets some necessary environment variables and logs some information
5.  `build/make/Makefile` contains the actual rule for building `python3`; this
    includes building all of `python3`'s dependencies first (and their
    dependencies, recursively); the actual package installation is performed
    with the `sage-spkg` program

Relocation
----------

It is not supported to move the `SAGE_ROOT` or `SAGE_LOCAL` directory
after building Sage.  If you do move the directories, you will have to
run ``make distclean`` and build Sage again from scratch.

For a system-wide installation, you have to build Sage as a "normal" user
and then as root you can change permissions. See the [Installation Guide](https://doc.sagemath.org/html/en/installation/source.html#installation-in-a-multiuser-environment)
for further information.

Redistribution
--------------

Your local Sage install is almost exactly the same as any "developer"
install. You can make changes to documentation, source, etc., and very
easily package the complete results up for redistribution just like we
do.

1.  To make a binary distribution with your currently installed packages,
    visit [sagemath/binary-pkg](https://github.com/sagemath/binary-pkg).

2.  To make your own source tarball of Sage, type:

        $ make dist

    The result is placed in the directory `dist/`.

Changes to Included Software
----------------------------

All software included with Sage is copyrighted by the respective authors
and released under an open source license that is __GPL version 3 or
later__ compatible. See [COPYING.txt](./COPYING.txt) for more details.

Sources are in unmodified (as far as possible) tarballs in the
`upstream/` directory. The remaining description, version
information, patches, and build scripts are in the accompanying
`build/pkgs/<packagename>` directory. This directory is
part of the Sage git repository.

<p align="center">
   Copyright (C) 2005-2025 The Sage Development Team
</p>
<p align="center">
   https://www.sagemath.org
</p>

