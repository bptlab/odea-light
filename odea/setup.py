from setuptools import setup, find_packages  # type: ignore


requirements = [
    'opyenxes>=0.3.0',
    'pandas>=1.0.4',
    'python-dotenv>=0.18.0',
    'pm4py>=2.2.8'
]


setup(
    name='odea_light',
    version='0.1',
    description='Quantitative Evaluation of Semantic Event Abstraction for Process Mining',
    url='https://gitlab.hpi.de/simon.remy/odea_lite/',
    author='Simon Remy and Jan Philipp Sachs',
    author_email='simon.remy@hpi.de, jan-philipp.sachs@hpi.de',
    keywords='odea oder_light process mining',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': [
            'typing-extensions>=3.7.4.3',
            'data-science-types',
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'pylint>=2.6.0',
        ]
    },
    include_package_data=True,
)
