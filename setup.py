from setuptools import setup

install_requirements = [
        'click',
        'requests',
        'garminconnect',
]

setup(
    name='Garmin-Proj',
    version='0.1.0dev',
    packages=['garminproj',],
    license='MIT License',
    long_description=open('README.md').read(),
    install_requires=install_requirements
)