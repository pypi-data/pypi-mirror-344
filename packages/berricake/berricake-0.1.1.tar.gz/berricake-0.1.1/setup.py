import codecs
import os
from setuptools import setup, find_packages
from Cython.Build import cythonize
import numpy

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.1.1'
DESCRIPTION = 'a modular simulation software. '
LONG_DESCRIPTION = 'BerriCake is a simulation software based on the modular concept. By writing the operating parameters of devices and the flow direction of data connections in text, it is possible to conduct transient simulation analysis of related devices.'

setup(
    name='berricake',
    version=VERSION,
    author="zhc1993",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    ext_modules=cythonize([
        'berricake/core/util.pyx',
        'berricake/core/time_controller.pyx',
        'berricake/core/base_module.pyx',
        'berricake/core/link.pyx',
        'berricake/core/parser.pyx',
        'berricake/core/manager.pyx',
        'berricake/berricake.pyx',

        'berricake/components/wind_module.pyx',
        'berricake/components/output.pyx',
        'berricake/components/epw_reader.pyx',
    ]),
    compiler_directives={'language_level': 3},
    include_dirs=[numpy.get_include()],  # 添加 numpy 头文件路径
    keywords=['python', 'simulate', 'berricake', 'windows'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=['numpy', 'scipy', 'colorama'],
    setup_requires=['Cython']
)