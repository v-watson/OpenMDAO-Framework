# pylint: disable-msg=C0111,C0103

import unittest
import logging

from openmdao.main import Model, Assembly, Component, Float
from openmdao.main.variable import INPUT, OUTPUT
from openmdao.lib.drivers.conmindriver import CONMINdriver

class PolyOrder2(Component):
    """Calculates a result given polynomial coefficients 
    for x**0, x**1, and x**2.
    """
    def __init__(self, name, parent):
        super(PolyOrder2, self).__init__(name, parent)
        Float('x', self, INPUT, default=0.)
        Float('c2', self, INPUT, default=1.0)
        Float('c1', self, INPUT, default=1.0)
        Float('c0', self, INPUT, default=0.0)
        Float('f_x', self, OUTPUT, default=0., doc='result of c2*x**2+c1*x+c0')
        
    def execute(self):
        self.f_x = self.x*(self.c2*self.x + self.c1) + self.c0
        
        
class Adder(Component):
    """Outputs the sum of its two inputs."""
    def __init__(self, name, parent):
        super(Adder, self).__init__(name, parent)
        Float('x1', self, INPUT, default=0.0)
        Float('x2', self, INPUT, default=0.0)
        Float('sum', self, OUTPUT, default=0.0)
        
    def execute(self):
        self.sum = self.x1 + self.x2
        
            
class MultiDriverTestCase(unittest.TestCase):

    def setUp(self):
        # Chop up the equations for the Rosen-Suzuki optimization problem
        # into 4 PolyOrder2 components and some Adders so that our driver
        # will iterate over more than one compnent
        top = Assembly('top', None)
        self.top = top
        PolyOrder2('comp1',top)
        PolyOrder2('comp2',top)
        PolyOrder2('comp3',top)
        PolyOrder2('comp4',top)
        
        # set up polynomials
        top.comp1.c1 = -5.0  # comp1 -->  x**2 - 5.0*x
        top.comp2.c1 = -5.0  # comp2 -->  x**2 - 5.0*x
        top.comp3.c2 = 2.0   # comp3 -->  2.0*x**2 - 21.0*x
        top.comp3.c1 = -21.0
        top.comp4.c1 = 7.0   # comp4 -->  x**2 + 7.0*x
        
        Adder('adder1', top)
        top.connect('comp1.f_x', 'adder1.x1')
        top.connect('comp2.f_x', 'adder1.x2')
        
        Adder('adder2', top)
        top.connect('comp3.f_x', 'adder2.x1')
        top.connect('comp4.f_x', 'adder2.x2')
        
        Adder('adder3', top)
        top.connect('adder1.sum', 'adder3.x1')
        top.connect('adder2.sum', 'adder3.x2')
        
        # create the first driver
        drv = CONMINdriver('driver1',top)
        drv.maxiters = 30
        drv.objective.value = 'adder3.sum+50.'
        drv.design_vars.value = ['comp1.x', 'comp2.x', 'comp3.x', 'comp4.x']
        drv.lower_bounds = [-10, -10, -10, -10]
        drv.upper_bounds = [99, 99, 99, 99]
        drv.constraints.value = [
            'comp1.x**2 + comp2.x**2 + comp3.x**2 + comp4.x**2 + comp1.x-comp2.x+comp3.x-comp4.x-8.0',
            'comp1.x**2 + 2.*comp2.x**2 + comp3.x**2 + 2.*comp4.x**2 - comp1.x - comp4.x -10.',
            '2.0*comp1.x**2 + comp2.x**2 + comp3.x**2 + 2.0*comp1.x - comp2.x - comp4.x -5.0',
        ]
        # expected optimal values
        self.opt_objective = 6.
        self.opt_design_vars = [0., 1., 2., -1.]
        

    def test_one_driver(self):
        self.assertEqual(['comp2', 'comp3', 'comp1', 'comp4', 'adder3'], 
                         self.top.driver1.sorted_components())
        self.top.run()
        self.assertAlmostEqual(self.opt_objective, 
                               self.top.driver1.objective.refvalue, places=2)
        self.assertAlmostEqual(self.opt_design_vars[0], 
                               self.top.comp1.x, places=1)
        self.assertAlmostEqual(self.opt_design_vars[1], 
                               self.top.comp2.x, places=2)
        self.assertAlmostEqual(self.opt_design_vars[2], 
                               self.top.comp3.x, places=2)
        self.assertAlmostEqual(self.opt_design_vars[3], 
                               self.top.comp4.x, places=1)
        
#    def test_2_drivers(self):
#        self.fail('test not implemented')
    
if __name__ == "__main__":
    
    #import cProfile
    #cProfile.run('unittest.main()', 'profout')
    
    #import pstats
    #p = pstats.Stats('profout')
    #p.strip_dirs()
    #p.sort_stats('time')
    #p.print_stats()
    #print '\n\n---------------------\n\n'
    #p.print_callers()
    #print '\n\n---------------------\n\n'
    #p.print_callees()
        
    unittest.main()


