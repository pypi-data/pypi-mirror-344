import re

import scikitplot
import scikitplot.version


def test_valid_scikitplot_version():
    # Verify that the scikit-plots version is a valid one (no .post suffix or other
    # nonsense). See NumPy issue gh-6431 for an issue caused by an invalid
    # version.
    version_pattern = r"^[0-9]+\.[0-9]+\.[0-9]+(|a[0-9]|b[0-9]|rc[0-9])"
    dev_suffix = r"((.dev0)|(\.dev0+\+git[0-9]{8}.[0-9a-f]{7}))"
    if scikitplot.version.release:
        res = re.match(version_pattern, scikitplot.__version__)
    else:
        res = re.match(version_pattern + dev_suffix, scikitplot.__version__)

    assert res is not None
    assert scikitplot.__version__


def test_version_submodule_members():
    """`scipy.version` may not be quite public, but we install it.

    So check that we don't silently change its contents.
    """
    for attr in ("version", "full_version", "short_version", "git_revision", "release"):
        assert hasattr(scikitplot.version, attr)
