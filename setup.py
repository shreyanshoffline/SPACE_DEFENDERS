try:
    from setuptools import setup
except Exception:
    # setuptools is required; distutils may be deprecated or removed in recent Python versions,
    # so raise a clear error telling the user how to install setuptools.
    raise RuntimeError(
        "setuptools is required to run setup.py; please install it with "
        "'python -m pip install setuptools'"
    )

APP = ['main.py']
DATA_FILES = ['assets', 'entities', 'screens', 'utils' ]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],  # optional, can remove if no icon
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)


