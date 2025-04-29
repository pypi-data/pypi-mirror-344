from setuptools import setup, find_packages

setup(
    name="toexe",  # نام بسته شما
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # وابستگی‌های پروژه (در صورت نیاز)
    description="A tool for converting Python scripts to EXE files with customizable options",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/toexe",  # URL پروژه در گیت‌هاب
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # نسخه پایتون مورد نیاز
)
