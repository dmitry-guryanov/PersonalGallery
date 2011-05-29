try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='PersonalGallery',
    version="0.1",
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
    	"Pylons>=0.9.7",
	"SQLAlchemy>=0.5"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'gallery': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors = {'gallery': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('controllers/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = gallery.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)