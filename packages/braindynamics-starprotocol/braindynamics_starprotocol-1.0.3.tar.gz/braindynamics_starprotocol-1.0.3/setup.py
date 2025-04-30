from setuptools import setup, Extension
import os
from Cython.Build import cythonize
import numpy as np

extensions = [  Extension(  name="sca.sca_cy", 
                            sources=[os.path.join("src", "braindynamics_starprotocol", "sca", "sca_cy.pyx")],
                            include_dirs=[np.get_include()])    ]

setup(  name="braindynamics_starprotocol",
        version="1.0.3",
        ext_modules=cythonize(extensions),
        include_dirs=[np.get_include()],
        options={
            'bdist_wheel': {
                'universal':True,
            },
        },
      )
