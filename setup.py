from setuptools import setup, find_packages

version = '2.0.19'

setup(
    name='Products.PasswordResetTool',
    version=version,
    description="Password reset tool for Plone",
    long_description=(
        open("README.rst").read() + "\n" +
        open("CHANGES.rst").read()),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='password reset plone',
    author='J. Cameron Cooper',
    author_email='prt@jcameroncooper.com',
    url='https://pypi.python.org/pypi/Products.PasswordResetTool',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'plone.app.testing',
        ],
    ),
    install_requires=[
        'setuptools',
        'plone.memoize',
        'zope.component',
        'zope.i18nmessageid',
        'zope.i18n',
        'zope.interface',
        'Products.CMFPlone',
        'Products.CMFCore',
        'Acquisition',
        'DateTime',
        'Zope2',
    ],
    )
