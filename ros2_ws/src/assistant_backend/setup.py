from setuptools import setup

package_name = 'assistant_backend'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Team Assistant Backend',
    maintainer_email='team@example.com',
    description='Backend node: preferences stored in SQLite',
    license='MIT',
    entry_points={
        'console_scripts': [
            'backend_node = assistant_backend.backend_node:main',
        ],
    },
)
