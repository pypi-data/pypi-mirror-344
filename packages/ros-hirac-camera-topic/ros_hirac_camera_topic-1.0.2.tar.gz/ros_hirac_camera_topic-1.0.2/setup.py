from setuptools import setup, find_packages

setup(
    name="ros_hirac_camera_topic",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    author="Anke Fischer-Janzen, Katrin-Misel Ponomarjova",
    author_email="katrinmisel@gmail.com",
    description="Changed from ros-sensor-topic. A utility package to find ROS topic names for color and depth streams.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/katrinmisel/ros_sensor_topic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)