from distutils.core import setup

setup(
    name='stratuslab-usecases',
    version='${project.version}',
    author='StratusLab',
    author_email='contact@stratuslab.eu',
    url='http://stratuslab.eu/',
    license='Apache 2.0',
    description='${project.description}',
    long_description=open('README.txt').read(),

    packages=['stratuslab_usecases',
              'stratuslab_usecases.cli',
              'stratuslab_usecases.api'],

    scripts=[
        'bin/stratus-run-usecases',
        ],

    install_requires=[
        # do not require these so that rpm installations can be tested
        #"stratuslab-libcloud-drivers",
        #"stratuslab-client",
        "nose",
        ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Distributed Computing',
        ],

)
