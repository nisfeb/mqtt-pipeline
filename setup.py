from setuptools import find_packages, setup

setup(
    name='mqtt_pipeline',
    version='0.1.0',
    description="""
        Library to permit pipeline-based processing of MQTT events with \
    premade middleware for convenience.
    """,
    author='~nisfeb',
    packages=find_packages(include=[
        'mqtt_pipeline',
        'mqtt_pipeline.*',
    ]),
    python_requires='>=3.6',
    install_requires=[
        'paho-mqtt>=1.6.1',
        'requests>=2.31.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': ['pytest>=4.4.1', 'pytest-runner'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
