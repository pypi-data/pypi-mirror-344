from setuptools import setup, find_packages

setup(
    name="gemini_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "requests",
        "python-dotenv",
        "pillow",
        "pydantic",
    ],
    entry_points={
        "console_scripts": [
            "gemini_agent=gemini_agent.cli:main",
        ],
    },
    description="An autonomous GUI agent powered by Google's Gemini API",
    author="Shubham Shinde",
    author_email="shubhamshindesunil@gmail.com",
    url="https://github.com/shubhamshnd/gemini-agent",
)