import gettext
import importlib.resources


# Setup translation with class-based gettext
try:
    with importlib.resources.as_file(
        importlib.resources.files("artefacts.cli.locales")
    ) as localedir:
        _translation = gettext.translation(
            "artefacts",
            localedir=str(localedir),
            fallback=True,
        )
except FileNotFoundError:
    #
    # Encountered in our trials with Python 3.10 and 3.11, so fallback to pkg_resources
    #
    # pkg_resources is removed from setuptools in Python 3.12. From there, importlib works.
    #
    from pkg_resources import resource_filename

    _localedir = resource_filename("artefacts.cli", "locales")
    _translation = gettext.translation(
        "artefacts",
        localedir=str(_localedir),
        fallback=True,
    )
# Available for other modules to import
localise = _translation.gettext
