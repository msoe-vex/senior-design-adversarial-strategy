from setuptools import setup, find_packages


setup(
    name='rr-field-entities-tipping-point',
    version='0.1',
    license='MIT',
    author="Raider Robotics",
    author_email='info@msoevex.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/msoe-vex/senior-design-adversarial-strategy',
    keywords='vex tipping point field entities raider robotics',
    install_requires=[
        'matplotlib==3.5.1',
        'numpy==1.22.2'
    ]
)