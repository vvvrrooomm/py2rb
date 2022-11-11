"""
Module that defines Tool functions and test runners/result for use with
the unittest library.
"""
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os
import posixpath
import re

def get_posix_path(path):
    """translates path to a posix path"""
    heads = []
    tail = path
    while tail != '':
        tail, head = os.path.split(tail)
        heads.append(head)
    return posixpath.join(*heads[::-1])

def run_with_stdlib(file_path, file_name=None):
    """Creates a test that runs a ruby file with the stdlib."""
    file_name = file_name if file_name else file_path

    class TestStdLib(unittest.TestCase):
        """Tests ruby code with the stdlib"""
        templ = {
            "rb_path": file_path, 
            "rb_unix_path": get_posix_path(file_path), 
            "rb_out_path": file_path + ".out",
            "rb_error": file_path + ".err",
            "name": file_name,
        }
        def reportProgres(self):
            """Should be overloaded by the test result class."""
    
        def runTest(self):
            """The actual test goes here."""
            cmd = (
                  'ruby "py2rb/builtins/module.rb" '
                  ' "%(rb_path)s" > "%(rb_out_path)s" 2> "%(rb_error)s"'
                  )% self.templ
            self.assertEqual(0, os.system(cmd))
            self.reportProgres()

        def __str__(self):
            return "%(rb_unix_path)s [1]: " % self.templ

    return TestStdLib

def compile_file_test(file_path, file_name=None):
    """Creates a test that tests if a file can be compiled by python"""
    file_name = file_name if file_name else file_path
    
    class CompileFile(unittest.TestCase):
        """Test if a file can be compiled by python."""

        templ = {
            "py_path": file_path, 
            "py_unix_path": get_posix_path(file_path), 
            "py_out_path": file_path + ".out",
            "py_error": file_path + ".err",
            "name": file_name,
        }
        def reportProgres(self):
            """Should be overloaded by the test result class"""

        def runTest(self):
            """The actual test goes here."""
            commands = (
                (
                'python "%(py_path)s" > '
                '"%(py_out_path)s" 2> "%(py_error)s"'
                ) % self.templ,
              )
            for cmd in commands:
                self.assertEqual(0, os.system(cmd))
                self.reportProgres()
        def __str__(self):
            return "%(py_unix_path)s [1]: " % self.templ
    return CompileFile


def compile_file_compare_test(file_path, file_name=None):
    """a test that compiles python and compares produced ruby"""
    file_name = file_name if file_name else file_path
    
    class CompileCompareFile(unittest.TestCase):
        """Test if compiled python matches static ruby."""
        name_path, ext = os.path.splitext(file_path)
        templ = {
            "py_path": file_path, 
            "py_dir_path": os.path.dirname(file_path),
            "py_unix_path": get_posix_path(file_path), 
            "py_out_path": file_path + ".out",
            "py_error": file_path + ".err",
            "rb_path": name_path + ".rb",
            "rb_expected_path": name_path + ".rb.expected",
            "name": file_name,
            "compiler_error": file_path + ".comp.err",
        }
        def reportProgres(self):
            """Should be overloaded by the test result class"""

        def runTest(self):
            """The actual test goes here."""
            commands = []
            commands.append(
                (
                'python "%(py_path)s" > '
                '"%(py_out_path)s" 2> "%(py_error)s"'
                ) % self.templ,
              )
            compile_command = (
                'python py2rb.py -p "%(py_dir_path)s" -r "%(py_path)s" -m -f -w -s 2> "%(compiler_error)s"'
                ) % self.templ
            commands.append(compile_command)

            for cmd in commands:
                self.assertEqual(0, os.system(cmd))
                self.reportProgres()
                       # Partial Match
            if os.path.exists(self.templ["rb_expected_path"]):
                # Fixed statement partial match
                f = open(self.templ["rb_expected_path"])
                g = open(self.templ["rb_path"])
                self.assertIn(
                    f.read(),
                    g.read()
                    )
                f.close()
                g.close()
            else:
                self.fail(f"file not found {self.templ['rb_expected_path']}")
            self.reportProgres()
        def __str__(self):
            return "%(py_unix_path)s [1]: " % self.templ
    return CompileCompareFile


def compile_and_run_file_test(file_path, file_name=None):
    """Creates a test that compiles and runs the python file as ruby"""
    file_name = file_name if file_name else file_path

    class CompileAndRunFile(unittest.TestCase):
        """Tests that a file can be compiled and run as ruby"""
        name_path, ext = os.path.splitext(file_path)
        templ = {
        "py_path": file_path, 
        "py_dir_path": os.path.dirname(file_path),
        "py_unix_path": get_posix_path(file_path),
        "py_out_path": file_path + ".out",
        "rb_path": name_path + ".rb",
        "rb_out_path": name_path + ".rb.out",
        "rb_out_expected_path": name_path + ".rb.expected_out",
        "rb_out_expected_in_path": name_path + ".rb.expected_in_out",
        "py_error": file_path + ".err",
        "rb_error": name_path + ".rb.err",
        "compiler_error": file_path + ".comp.err",
        "name": file_name,
        "cmd_out": name_path + ".cmd.txt",
        }
        def reportProgres(self):
            """Should be overloaded by the test result class"""

        def runTest(self):
            """The actual test goes here."""
            commands = []
            python_command = (
                'python "%(py_path)s" > "%(py_out_path)s" 2> '
                '"%(py_error)s"'
                ) % self.templ
            commands.append(python_command)
            compile_command = (
                'python py2rb.py -p "%(py_dir_path)s" -r "%(py_path)s" -m -f -w -s 2> "%(compiler_error)s"'
                ) % self.templ
            commands.append(compile_command)
            ruby_command = (
                'ruby -I py2rb/builtins "%(rb_path)s" > "%(rb_out_path)s" 2> '
                '"%(rb_error)s"' 
                ) % self.templ
            commands.append(ruby_command)
            with open(self.templ['cmd_out'], mode = 'w') as fh:
                for cmd in commands:
                    fh.write(cmd + '\n')
                    #print(cmd) # debug
                    self.assertEqual(0, os.system(cmd))
                    self.reportProgres()
            # Partial Match
            if os.path.exists(self.templ["rb_out_expected_in_path"]):
                # Fixed statement partial match
                f = open(self.templ["rb_out_expected_in_path"])
                g = open(self.templ["rb_out_path"])
                self.assertIn(
                    f.read(),
                    g.read()
                    )
                f.close()
                g.close()
            else: # Full text match
                # Fixed sentence matching
                if os.path.exists(self.templ["rb_out_expected_path"]):
                    expected_file_path = self.templ["rb_out_expected_path"]
                else: # Dynamic sentence matching
                    expected_file_path = self.templ["py_out_path"]
                f = open(expected_file_path, 'r')
                g = open(self.templ["rb_out_path"])
                self.assertEqual(
                    f.readlines(),
                    g.readlines()
                    )
                f.close()
                g.close()
            self.reportProgres()

        def __str__(self):
            return "%(py_unix_path)s [4]: " % self.templ

    return CompileAndRunFile

def compile_and_run_file_failing_test(*a, **k):
    """Turn a test to a failing test"""
    _class = compile_and_run_file_test(*a, **k)

    class FailingTest(_class):
        """Failing test"""
        @unittest.expectedFailure
        def runTest(self):
            return super(FailingTest, self).runTest()

    return FailingTest

