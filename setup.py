import codecs
from setuptools import setup
from setuptools import find_packages

entry_points = {
    'console_scripts': [
    ],
    "z3c.autoinclude.plugin": [
        'target = nti.app',
    ],
}

TESTS_REQUIRE = [
    'nti.app.testing',
    'nti.testing',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.app.orgsync',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI OrgSync App Layer",
    long_description=(
        _read('README.rst')
        + '\n\n'
        + _read("CHANGES.rst")
    ),
    license='Apache',
    keywords='pyramid orgsync',
    classifiers=[
        'Framework :: Zope3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/OpenNTI/nti.app.orgsync",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti', 'nti.app'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'nti.app.spark',
        'nti.orgsync',
        'nti.orgsync_rdbms',
        'nti.orgsync_spark',
        'nti.schema',
        'nti.traversal',
        'pyramid',
        'python-redis-lock',
        'six',
        'zope.cachedescriptors',
        'zope.component',
        'zope.container',
        'zope.event',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.location',
        'zope.security',
        'zope.traversing',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
        ],
    },
    entry_points=entry_points,
)
