import subprocess

from AvidaScripts import get_avida_executable_path


def test_get_avida_executable_path():

    # run twice to test caching
    for __ in range(2):
        avida_executable_path = get_avida_executable_path()

        # Run the command
        process = subprocess.run(
            [avida_executable_path, "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        assert process.returncode == 0 and "Avida" in process.stdout
