from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nifty_agent",
    version="0.1.0",
    author="Manus",
    author_email="contact@manus.im",
    description="A vision-based GUI automation agent powered by a low-resource LLM.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/nifty_agent", # Replace with your repo URL
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
            "nifty-agent=nifty_agent.agent:main_cli",
        ],
    },
)


