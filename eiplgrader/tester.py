import unittest
import tempfile
import importlib
import os

class CodeTester:

    def __init__(self, code, test_cases):
        self.code = code
        print(self.code)
        self.test_cases = test_cases

    def test_user_function(self, args, expected_output):
        global foo
        assert foo(*args) == expected_output

    def run_tests(self):

        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
            temp_file.write(self.code.encode('utf-8'))
            temp_file_path = temp_file.name

        spec = importlib.util.spec_from_file_location("temp_module", temp_file_path)
        temp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(temp_module)

        os.remove(temp_file_path)

        globals()['foo'] = temp_module.foo

        test_suite = unittest.TestSuite()
        for test_case in self.test_cases:
            test_suite.addTest(
                unittest.FunctionTestCase(
                    lambda: self.test_user_function(*test_case),
                )
            )
        
        runner = unittest.TextTestRunner()
        result = runner.run(test_suite)
        return result