# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os
from distutils.version import LooseVersion
# this contains imports plugins that configure py.test for astropy tests.
# by importing them here in conftest.py they are discoverable by py.test
# no matter how it is invoked within the source tree.

from astropy.version import version as astropy_version

if LooseVersion(astropy_version) < LooseVersion('2.0.3'):
    # Astropy is not compatible with the standalone plugins prior this while
    # astroquery requires them, so we need this workaround. This will mess
    # up the test header, but everything else will work.
    from astropy.tests.pytest_plugins import (PYTEST_HEADER_MODULES,
                                              enable_deprecations_as_exceptions,
                                              TESTED_VERSIONS)
elif astropy_version < '3.0':
    # With older versions of Astropy, we actually need to import the pytest
    # plugins themselves in order to make them discoverable by pytest.
    from astropy.tests.pytest_plugins import *
else:
    # As of Astropy 3.0, the pytest plugins provided by Astropy are
    # automatically made available when Astropy is installed. This means it's
    # not necessary to import them here, but we still need to import global
    # variables that are used for configuration.
    from pytest_astropy_header.display import PYTEST_HEADER_MODULES, TESTED_VERSIONS

from astropy.tests.helper import enable_deprecations_as_exceptions

# Add astropy to test header information and remove unused packages.
# Pytest header customisation was introduced in astropy 1.0.

try:
    PYTEST_HEADER_MODULES['Astropy'] = 'astropy'
    del PYTEST_HEADER_MODULES['h5py']
    del PYTEST_HEADER_MODULES['Scipy']
    del PYTEST_HEADER_MODULES['Matplotlib']
    del PYTEST_HEADER_MODULES['Pandas']
except (NameError, KeyError):
    pass

enable_deprecations_as_exceptions()



# This is to figure out the affiliated package version, rather than
# using Astropy's
from .version import version, astropy_helpers_version


packagename = os.path.basename(os.path.dirname(__file__))
TESTED_VERSIONS[packagename] = version
TESTED_VERSIONS['astropy_helpers'] = astropy_helpers_version
