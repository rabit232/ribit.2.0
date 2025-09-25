from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ribit_2_0",
    version="2.0.0",
    author="Manus AI & rabit232",
    author_email="contact@manus.im",
    description="Enhanced AI agent with production-ready LLM emulator, ROS integration, Matrix bot, Jina.ai search, and emotional intelligence for GUI automation and robotic control.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rabit232/ribit.2.0",
    project_urls={
        "Bug Reports": "https://github.com/rabit232/ribit.2.0/issues",
        "Source": "https://github.com/rabit232/ribit.2.0",
        "Documentation": "https://github.com/rabit232/ribit.2.0#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    keywords="ai agent automation robotics ros matrix llm emotional-intelligence gui-automation computer-vision",
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "ros1": ["rospy"],
        "ros2": ["rclpy>=3.0.0", "std_msgs", "geometry_msgs", "sensor_msgs"],
        "performance": ["redis>=4.5.0", "celery>=5.3.0"],
        "analytics": ["textstat>=0.7.0", "wordcloud>=1.9.0"],
        "dev": ["pytest>=6.0.0", "pytest-asyncio>=0.18.0"],
    },
    entry_points={
        "console_scripts": [
            "ribit-2-0=ribit_2_0.agent:main_cli",
            "ribit-matrix-bot=run_matrix_bot:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ribit_2_0": ["*.txt", "*.md"],
    },
    zip_safe=False,
)


