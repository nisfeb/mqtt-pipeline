from setuptools import find_packages, setup
import subprocess
import os
from setuptools.command.develop import develop
from setuptools.command.install import install


class PreDevelopCommand(develop):
    """Pre-installation for development mode."""
    def run(self):
        try:
            # Check if we're in a git repository
            subprocess.check_call(['git', 'rev-parse', '--is-inside-work-tree'])
            # Initialize submodules
            subprocess.check_call(['git', 'submodule', 'update', '--init', '--recursive'])

            # Run make proto in the specific directory
            proto_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'mqtt_pipeline', 'middleware', 'meshtastic')
            if os.path.exists(proto_dir):
                print(f"Running 'make proto' in {proto_dir}")
                subprocess.check_call(['make', 'proto'], cwd=proto_dir)
            else:
                print(f"Warning: Directory {proto_dir} does not exist, skipping 'make proto'")
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
        except Exception as e:
            print(f"Error during pre-installation: {e}")
        develop.run(self)


class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        try:
            # Check if we're in a git repository
            subprocess.check_call(['git', 'rev-parse', '--is-inside-work-tree'])
            # Initialize submodules
            subprocess.check_call(['git', 'submodule', 'update', '--init', '--recursive'])

            # Run make proto in the specific directory
            proto_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'mqtt_pipeline', 'middleware', 'meshtastic')
            if os.path.exists(proto_dir):
                print(f"Running 'make proto' in {proto_dir}")
                subprocess.check_call(['make', 'proto'], cwd=proto_dir)
            else:
                print(f"Warning: Directory {proto_dir} does not exist, skipping 'make proto'")
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
        except Exception as e:
            print(f"Error during pre-installation: {e}")
        install.run(self)


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
        'protobuf>=6.30.1',
        'meshtastic>=2.6.0',
    ],
    extras_require={
        'dev': ['pytest>=4.4.1', 'pytest-runner'],
    },
    cmdclass={
        'develop': PreDevelopCommand,
        'install': PreInstallCommand,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
