from setuptools import setup

# Basic project information
setup(
    name='lhasa-kata',  # Choose a unique name for your project
    version='0.1',
    author='Micheal Nestor',
    description='Lhasa Kata Completed after attending Exploring Scientific Software Development: In Collaboration with Lhasa',
    py_modules=['kata'],  # Specify the script as a module
    install_requires=[
        'beautifulsoup4',
        # 'xmltodict'
    ]
)
