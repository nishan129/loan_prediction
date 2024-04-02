from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    
    requirements_list:List[str] = []
    
    return requirements_list
    

setup(
    name= "Loan Prediction",
    version="0.0.0",
    description="LoanPredict Pro is a cutting-edge machine learning application designed to revolutionize the loan approval process. Leveraging state-of-the-art predictive algorithms, LoanPredict Pro provides financial institutions and borrowers with accurate, efficient, and fair loan approval decisions. ",
    author="Nishant Borkar",
    author_email="nishantborkar139@gmail.com",
    packages= find_packages(),
    install_requires = get_requirements()
)