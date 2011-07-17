'''runtests.py - discovers and runs all the tests in the tests folder'''
import unittest

if __name__ == "__main__":
    try:
        skindepth_tests = unittest.TestLoader().discover(start_dir = "tests")
        unittest.TextTestRunner(verbosity=2).run(skindepth_tests)
    except AttributeError:
        pass
    # Running on Python 2.6 or lower, try importing unittest2 http://pypi.python.org/pypi/unittest2
    try:
        import unittest2
        skindepth_tests = unittest2.TestLoader().discover(start_dir = "tests")
        unittest2.TextTestRunner(verbosity=2).run(skindepth_tests)
    except ImportError:
        pass
            
    # No unittest2, try loading the tests module as a fallback
    skindepth_tests = unittest.TestLoader().loadTestsFromModule("tests")
    unittest.TextTestRunner(verbosity=2).run(skindepth_tests)