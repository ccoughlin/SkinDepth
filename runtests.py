import unittest

if __name__=="__main__":
    skindepth_tests = unittest.TestLoader().discover(start_dir = "tests")
    unittest.TextTestRunner(verbosity=2).run(skindepth_tests)