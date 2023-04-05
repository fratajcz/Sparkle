"""Test public methods of solver class."""

import shutil

from unittest import TestCase, mock
from pathlib import Path

from sparkle_help.configuration_scenario import ConfigurationScenario
from sparkle_help.solver import Solver


class TestConfigurationScenario(TestCase):
    """Class bundling all tests regarding ConfigurationScenario."""
    def setUp(self):
        """Setup executed before each test."""
        self.solver_path = Path("tests", "test_files", "Solvers", "Test-Solver")
        self.solver = Solver(self.solver_path)

        self.source_instance_directory = Path("tests/test_files/"
                                              "Instances/Test-Instance-Set")

        self.run_number = 2

        self.parent_directory = Path("tests/test_files/test_configurator")
        self.parent_directory.mkdir(parents=True, exist_ok=True)

        self.scenario = ConfigurationScenario(self.solver,
                                              self.source_instance_directory,
                                              self.run_number, False)

    def tearDown(self):
        """Cleanup executed after each test."""
        shutil.rmtree(self.parent_directory, ignore_errors=True)

    def test_configuration_scenario_init(self):
        """Test if all variables that are set in the init are correct."""
        mock.patch("sparkle_help.sparkle_global_help.solver_list_path",
                   return_value="tests/test_files/reference_files/"
                   "sparkle_solver_list.txt")

        self.assertEqual(self.scenario.solver, self.solver)
        self.assertEqual(self.scenario.source_instance_directory,
                         self.source_instance_directory)
        self.assertEqual(self.scenario.use_features, False)
        self.assertEqual(self.scenario.feature_data, None)
        self.assertEqual(self.scenario.name,
                         f"{self.solver.name}_{self.source_instance_directory.name}")

    def test_configuration_scenario_check_scenario_directory(self):
        """Test if create_scenario() correctly creates the scenario directory."""
        with mock.patch("sparkle_help.sparkle_global_help.solver_list_path",
                        return_value="tests/test_files/reference_files/"
                        "sparkle_solver_list.txt"):
            self.scenario.create_scenario(self.parent_directory)

        self.assertEqual(self.scenario.directory.is_dir(), True)
        self.assertEqual((self.scenario.directory
                          / "outdir_train_configuration").is_dir(),
                         True)
        self.assertEqual((self.scenario.directory / "tmp").is_dir(), True)

        self.assertEqual((self.scenario.directory
                          / self.solver.get_pcs_file().name).is_file(), True)

    def test_configuration_scenario_check_result_directory(self):
        """Test if create_scenario() creates the result directory."""
        with mock.patch("sparkle_help.sparkle_global_help.solver_list_path",
                        return_value="tests/test_files/reference_files/"
                        "sparkle_solver_list.txt"):
            self.scenario.create_scenario(self.parent_directory)

        self.assertEqual(self.scenario.result_directory.is_dir(), True)

    def test_configuration_scenario_check_run_folders(self):
        """Test if create_scenario() correctly creates the run directories."""
        with mock.patch("sparkle_help.sparkle_global_help.solver_list_path",
                        return_value="tests/test_files/reference_files/"
                        "sparkle_solver_list.txt"):
            self.scenario.create_scenario(self.parent_directory)

        for i in range(self.run_number):
            run_path = self.scenario.directory / str(i + 1)
            self.assertEqual(run_path.is_dir(), True)
            self.assertEqual((run_path / "PbO-CCSAT").is_file(), True)
            self.assertEqual((run_path / "tmp").is_dir(), True)

    def test_configuration_scenario_check_instance_directory(self):
        """Test if create_scenario() creates the instance directory."""
        with mock.patch("sparkle_help.sparkle_global_help.solver_list_path",
                        return_value="tests/test_files/reference_files/"
                        "sparkle_solver_list.txt"):
            self.scenario.create_scenario(self.parent_directory)

        self.assertEqual(self.scenario.instance_directory.is_dir(), True)

    def test_configuration_scenario_check_instances(self):
        """Test if create_scenario() copies instances and creates instance list file."""
        with mock.patch("sparkle_help.sparkle_global_help.solver_list_path",
                        return_value="tests/test_files/reference_files/"
                        "sparkle_solver_list.txt"):
            self.scenario.create_scenario(self.parent_directory)

        instance_file_path = self.scenario.directory / self.scenario.instance_file_name
        self.assertEqual(instance_file_path.is_file(), True)
        instance_file = instance_file_path.open()
        instance_file_content = instance_file.read()
        self.assertEqual(instance_file_content,
                         "../../instances/Test-Instance-Set/test_instance_1.cnf\n")

        instance_file.close()

    def test_configuration_scenario_check_scenario_file(self):
        """Test if create_scenario() correctly creates the scenario file."""
        with mock.patch.object(Solver, "is_deterministic") as mock_deterministic:
            mock_deterministic.return_value = "0"

            self.scenario.create_scenario(self.parent_directory)

        scenario_file_path = self.scenario.directory / self.scenario.scenario_file
        reference_scenario_file = Path("tests", "test_files", "reference_files",
                                       "scenario_file.txt")

        # Use to show full diff of file
        # self.maxDiff = None

        self.assertEqual(scenario_file_path.is_file(), True)
        self.assertEqual(scenario_file_path.open().read(),
                         reference_scenario_file.open().read())
