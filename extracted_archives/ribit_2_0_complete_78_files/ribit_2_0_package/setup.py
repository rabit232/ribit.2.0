from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ribit_2_0",
    version="0.1.0",
    author="Manus",
    author_email="contact@manus.im",
    description="A vision-based GUI automation agent powered by a low-resource LLM, now known as Ribit 2.0.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/ribit_2_0", # This will be updated with the actual GitHub URL later
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyautogui",
        "pynput",
        "Pillow",
        "numpy",
        "numba",
        "opencv-python",
    ],
    entry_points={
        "console_scripts": [
            "ribit-2-0=ribit_2_0.agent:main_cli",
        ],
    },
)


