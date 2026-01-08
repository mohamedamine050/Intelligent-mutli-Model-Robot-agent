from setuptools import setup
import os
from glob import glob

package_name = 'robot_sensors'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ⚠️ CETTE LIGNE EST CRITIQUE : 
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),  # ← Vérifie qu'elle existe ! 
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Sensor nodes',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ultrasonic_node = robot_sensors.ultrasonic_node:main',
            'esp32_cam_node = robot_sensors.esp32_cam_node:main',
            'stereo_depth_node = robot_sensors.stereo_depth_node:main',
        ],
    },
)