import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.0.3'
DESCRIPTION = 'eazyml-counterfactual from EazyML family for counterfactual explanations, prescriptive analytics, and actionable insights to optimize predictive outcomes.'



# Setting up
setup(
    name="eazyml-counterfactual",
    version=VERSION,
    author="EazyML",
    author_email="admin@eazyml.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    package_dir={"eazyml_counterfactual":"./eazyml_counterfactual"},
    # Includes additional non-Python files in the package.
    package_data={'' : ['*.py', '*.so', '*.dylib', '*.pyd']},
    install_requires=[
                      'openpyxl',
                      'scipy',
                      'cryptography',
                      'pyyaml',
                      'requests',
                      'eazyml-automl'
                      ],
    extras_require={
        ':python_version<="3.7"': ['pandas==1.3.*', 'scikit-learn==1.0.*'],
        ':python_version=="3.8"': ['pandas>=2.0.3', 'scikit-learn==1.3.*'],
        ':python_version=="3.9"': ['pandas>=2.2.3', 'scikit-learn==1.3.*'],
        ':python_version=="3.10"': ['pandas>=2.2.3', 'scikit-learn==1.3.*'],
        ':python_version=="3.11"': ['pandas>=2.2.3', 'scikit-learn==1.3.*'],
        ':python_version>"3.11"': ['pandas>=2.2.3', 'scikit-learn==1.3.*']
    },
    keywords=['counterfactuals', 'prescriptive-analytics', 'optimal-decision',
              'what-if-analysis', 'actionable-insights',
              'prediction-optimization', 'causal-inference',
              'machine-learning', 'ml-api', 'explainable-ai'],
    url="https://eazyml.com/",
    project_urls={
        "Documentation": "https://docs.eazyml.com/",
        "Homepage": "https://eazyml.com/",
        "Contact Us": "https://eazyml.com/trust-in-ai",
        "eazyml-automl": "https://pypi.org/project/eazyml-automl/",
        "eazyml-counterfactual": "https://pypi.org/project/eazyml-counterfactual/",
        "eazyml-xai": "https://pypi.org/project/eazyml-xai/",
        "eazyml-xai-image": "https://pypi.org/project/eazyml-xai-image/",
        "eazyml-insight": "https://pypi.org/project/eazyml-insight/",
        "eazyml-data-quality": "https://pypi.org/project/eazyml-data-quality/",
    },
    similar_projects={
        'eazyml-data-quality' : "https://pypi.org/project/eazyml-data-quality/",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7"
)
