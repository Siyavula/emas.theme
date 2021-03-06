from setuptools import setup, find_packages
import os

version = '1.35'

setup(name='emas.theme',
      version=version,
      description="Theme for Everything Maths & Science Plone site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['emas'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.theming',
          'rhaptos.xmlfile',
          'rhaptos.cnxmltransforms',
          'upfront.shorturl',
          'asciimathml',
          'ordereddict',
      ],
      tests_require=[
        'plone.app.registry',
        'rhaptos.xmlfile',
        'upfront.shorturl',
        'asciimathml',
      ],
      extras_require={
        'test': [
          'plone.app.registry',
          'plone.app.testing',
          'rhaptos.xmlfile',
          'upfront.shorturl',
          'asciimathml',
        ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
