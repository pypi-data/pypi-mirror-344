from setuptools import setup, find_packages

setup(
    name='ArtusAPI',
    version='1.1.2',
    description='API to control Artus Family of Robots by Sarcomere Dynamics Inc',
    # package_dir={'': '/'},  # tells setuptools that your packages are under src
    packages=find_packages(exclude=['data*', 'examples*', 'tests*','venv*', 'urdf*', 'ros2*']),
    author='Sarcomere Dynamics Inc.',
    install_requires=[
        'psutil==5.9.8',
        'esptool',
        'pyserial==3.5',
        'tqdm',
        'pyyaml'
    ]
    # packages=find_packages(where='/'),
    # other setup configurations
)