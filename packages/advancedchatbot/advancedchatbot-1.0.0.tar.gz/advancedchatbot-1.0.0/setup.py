from setuptools import setup, find_packages

setup(
    name='advancedchatbot',
    version='1.0.0',
    description='An advanced chatbot that can chat, code, and browse the web.',
    author='kkyian',
    packages=find_packages(),
    install_requires=[],  # No external packages needed
    entry_points={
        'console_scripts': [
            'advancedchatbot = advancedchatbot.main:run_chatbot'
        ]
    },
    python_requires='>=3.7'
)

