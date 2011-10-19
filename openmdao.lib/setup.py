
# pylint: disable-msg=F0401

import os,sys
from setuptools import setup, find_packages

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here,
                                                 'src',
                                                 'openmdao',
                                                 'lib')))
import releaseinfo
version = releaseinfo.__version__

setup(name='openmdao.lib',
      version=version,
      description="OpenMDAO Standard Library",
      long_description="""\
Component, Driver, and Variable plugins for OpenMDAO
""",
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Topic :: Scientific/Engineering',
      ],
      keywords='optimization multidisciplinary multi-disciplinary analysis',
      author='',
      author_email='',
      url='http://openmdao.org/docs/srcdocs/packages/openmdao.lib.html',
      license='Apache License, Version 2.0',
      namespace_packages=["openmdao"],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      package_data={'openmdao.lib': ['components/test/*.inp']},
      include_package_data=True,
      test_suite='nose.collector',
      zip_safe=False,
      install_requires=[
          'setuptools',
          'openmdao.main',
          'conmin==1.0.1',
          'newsumt==1.1.0',
          'Pyevolve==0.6',
          'ordereddict',
          'scipy',
          #'ffnet>=0.7'
          ],
      entry_points="""
      [openmdao.driver]
      openmdao.lib.drivers.broydensolver.BroydenSolver = openmdao.lib.drivers.broydensolver:BroydenSolver
      openmdao.lib.drivers.caseiterdriver.CaseIteratorDriver = openmdao.lib.drivers.caseiterdriver:CaseIteratorDriver
      openmdao.lib.drivers.conmindriver.CONMINdriver = openmdao.lib.drivers.conmindriver:CONMINdriver
      openmdao.lib.drivers.doedriver.DOEdriver = openmdao.lib.drivers.doedriver:DOEdriver
      openmdao.lib.drivers.genetic.Genetic = openmdao.lib.drivers.genetic:Genetic
      openmdao.lib.drivers.gradient.SensitivityDriver = openmdao.lib.drivers.sensitivity:SensitivityDriver
      openmdao.lib.drivers.iterate.FixedPointIterator = openmdao.lib.drivers.iterate:FixedPointIterator
      openmdao.lib.drivers.iterate.IterateUntil = openmdao.lib.drivers.iterate:IterateUntil
      openmdao.lib.drivers.newsumtdriver.NEWSUMTdriver = openmdao.lib.drivers.newsumtdriver:NEWSUMTdriver
      openmdao.lib.drivers.simplecid.SimpleCaseIterDriver = openmdao.lib.drivers.simplecid:SimpleCaseIterDriver
      openmdao.lib.drivers.sensitivity.SensitivityDriver = openmdao.lib.drivers.sensitivity:SensitivityDriver

      [openmdao.component]
      openmdao.lib.components.expected_improvement.ExpectedImprovement = openmdao.lib.components.expected_improvement:ExpectedImprovement
      openmdao.lib.components.expected_improvement_multiobj.MultiObjExpectedImprovement = openmdao.lib.components.expected_improvement_multiobj:MultiObjExpectedImprovement
      openmdao.lib.components.external_code.ExternalCode = openmdao.lib.components.external_code:ExternalCode
      openmdao.lib.components.metamodel.MetaModel = openmdao.lib.components.metamodel:MetaModel
      openmdao.lib.components.mux.Mux = openmdao.lib.components.mux:Mux
      openmdao.lib.components.mux.DeMux = openmdao.lib.components.mux:DeMux
      openmdao.lib.components.broadcaster.Broadcaster = openmdao.lib.components.broadcaster:Broadcaster
      openmdao.lib.components.pareto_filter.ParetoFilter = openmdao.lib.components.pareto_filter:ParetoFilter

      [openmdao.differentiator]
      openmdao.lib.differentiators.finite_difference.FiniteDifference = openmdao.lib.differentiators.finite_difference:FiniteDifference
      
      [openmdao.variable]
      openmdao.lib.datatypes.array.Array = openmdao.lib.datatypes.array:Array
      openmdao.lib.datatypes.enum.Enum = openmdao.lib.datatypes.enum:Enum
      openmdao.lib.datatypes.file.File = openmdao.lib.datatypes.file:File
      openmdao.lib.datatypes.float.Float = openmdao.lib.datatypes.float:Float
      openmdao.lib.datatypes.int.Int = openmdao.lib.datatypes.int:Int
      
      [openmdao.surrogatemodel]
      openmdao.lib.surrogatemodels.kriging_surrogate = openmdao.lib.surrogatemodels.kriging_surrogate:KrigingSurrogate
      openmdao.lib.surrogatemodels.logistic_regression = openmdao.lib.surrogatemodels.logistic_regression:LogisticRegression
      openmdao.lib.surrogatemodels.nn_surrogate = openmdao.lib.surrogatemodels.nn_surrogate:NeuralNet
      
      [openmdao.optproblems]
      openmdao.lib.optproblems.sellar.SellarProblem = openmdao.lib.optprobelems.sellar:SellarProblem
      openmdao.lib.optproblems.branin.BraninProblem = openmdao.lib.optprobelems.branin:BraninProblem
      
      """,
      )

      # Optproblem entry points (commented for now)
      #openmdao.lib.optproblems.sellar.Discipline1 = openmdao.lib.optproblems.sellar:Discipline1
      #openmdao.lib.optproblems.sellar.Discipline2 = openmdao.lib.optproblems.sellar:Discipline2
      #openmdao.lib.optproblems.sellar.Discipline1_WithDerivatives = openmdao.lib.optproblems.sellar:Discipline1_WithDerivatives
      #openmdao.lib.optproblems.sellar.Discipline2_WithDerivatives = openmdao.lib.optproblems.sellar:Discipline2_WithDerivatives
      #openmdao.lib.optproblems.sellar.SellarProblem = openmdao.lib.optproblems.sellar:SellarProblem
