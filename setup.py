from setuptools import setup, find_packages

version = '1.2'

setup(name='Products.PasswordResetTool',
      version=version,
      description="password reset tool for Plone",
      long_description="""\
""",
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='password reset plone',
      author='J. Cameron Cooper',
      author_email='prt@jcameroncooper.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'Products.PloneTestCase',
        ]
      ),
      install_requires=[
          'setuptools',
          'zope.interface',
          'Products.CMFCore'
          # 'DateTime',
          # 'Zope2',
      ],
      )
