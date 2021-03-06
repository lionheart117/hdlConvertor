import unittest

from tests.notebook_test import NotebookTC
from tests.test_basic_hdl_sim_model_from_verilog import BasicHdlSimModelFromVerilogTC
from tests.test_icarus_verilog_testsuite import IcarusVerilogTestsuiteTC
from tests.test_sv2017_std_examples_parse import Sv2017StdExamplesParseTC
from tests.test_verilator_testsuite import VerilatorTestsuiteTC
from tests.test_verilog_conversion import VerilogConversionTC
from tests.test_verilog_preproc import VerilogPreprocTC
from tests.test_verilog_preproc_grammar import VerilogPreprocGrammarTC
from tests.test_verilog_preproc_include import VerilogPreprocIncludeTC
from tests.test_verilog_preproc_macro_db_api import VerilogPreprocMacroDbApiTC
from tests.test_vhdl_conversion import VhdlConversionTC
from tests.test_vunit_testsuite import VUnitTestsuiteTC
from tests.test_yosys_testsuite import YosysTestsuiteTC
from tests.time_logging_test_runner import TimeLoggingTestRunner
from tests.test_ghdl_testsuite import GhdlTestsuiteTCs
from tests.test_uvvm_testsuite import UVVMTestsuite


def main_test_suite():
    suite = unittest.TestSuite()
    tcs = [
        VerilogPreprocGrammarTC,
        VerilogPreprocTC,
        VerilogPreprocIncludeTC,
        VerilogPreprocMacroDbApiTC,
        VerilogConversionTC,
        VhdlConversionTC,
        Sv2017StdExamplesParseTC,
        IcarusVerilogTestsuiteTC,
        VerilatorTestsuiteTC,
        YosysTestsuiteTC,
        VUnitTestsuiteTC,
        UVVMTestsuite,
        BasicHdlSimModelFromVerilogTC,
        NotebookTC,
    ] + GhdlTestsuiteTCs
    for tc in tcs:
        suite.addTest(unittest.makeSuite(tc))

    return suite


if __name__ == "__main__":
    suite = main_test_suite()
    runner = TimeLoggingTestRunner(verbosity=3)

    try:
        from concurrencytest import ConcurrentTestSuite, fork_for_tests
        useParallerlTest = True
    except ImportError:
        # concurrencytest is not installed, use regular test runner
        useParallerlTest = False
    # useParallerlTest = False

    if useParallerlTest:
        # Run same tests across 4 processes
        concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests())
        runner.run(concurrent_suite)
    else:
        runner.run(suite)
