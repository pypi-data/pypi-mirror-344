"""
Tasks for maintaining the project.

Execute 'inv[oke] --list' for a list of dev tasks.
"""

import fnmatch
import glob
import os
import platform
import shutil
import webbrowser
from pathlib import Path

from invoke import task
from rich.console import Console

console = Console()
ROOT_DIR = Path(__file__).parent.resolve()
TEST_DIR = ROOT_DIR / "tests"
SOURCE_DIR = ROOT_DIR / "visionsim"
EXAMPLE_DIR = ROOT_DIR / "examples"
SCRIPTS_DIR = ROOT_DIR / "scripts"
COVERAGE_FILE = ROOT_DIR / ".coverage"
COVERAGE_DIR = ROOT_DIR / "htmlcov"
COVERAGE_REPORT = COVERAGE_DIR / "index.html"
DOCS_DIR = ROOT_DIR / "docs"
DOCS_INDEX = DOCS_DIR / "build" / "html" / "index.html"
DOCS_STATIC = DOCS_DIR / "source" / "_static"
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR, EXAMPLE_DIR, SCRIPTS_DIR, DOCS_DIR]]


def _delete_file(file, except_patterns=None):
    if os.path.isfile(file):
        console.print(f"Removing file {file}.")
        os.remove(file)
    elif os.path.isdir(file):
        if except_patterns is None:
            console.print(f"Removing directory {file}.")
            shutil.rmtree(file, ignore_errors=True)
        else:
            console.print(f"Purging directory {file}.")
            for dirpath, dirnames, filenames in os.walk(file):
                # Remove regular files, ignore directories
                for filename in filenames:
                    file = os.path.join(dirpath, filename)
                    if any(fnmatch.fnmatch(file, pattern) for pattern in except_patterns):
                        console.print(f"\tKeeping file {file}.")
                    else:
                        console.print(f"\tRemoving file {file}.")
                        os.remove(file)
                # Remove empty directories
                if not dirnames and not filenames:
                    console.print(f"\tRemoving directory {file}.")
                    shutil.rmtree(dirpath, ignore_errors=True)


def _delete_pattern(pattern):
    for file in glob.glob(os.path.join("**", pattern), recursive=True):
        _delete_file(file)


def _run(c, command, **kwargs):
    return c.run(command, pty=platform.system() != "Windows", **kwargs)


@task
def format(c):
    """Format code (and sort imports)"""
    python_dirs_string = " ".join(PYTHON_DIRS + glob.glob(os.path.join(ROOT_DIR, "*.py")))
    _run(c, f"ruff check --select I --fix {python_dirs_string} {__file__}")
    _run(c, f"ruff format {python_dirs_string}")


@task
def lint(c):
    """Lint code with ruff"""
    _run(c, f"ruff check --extend-select I {' '.join(PYTHON_DIRS)} {__file__}")


@task
def test(c):
    """Run tests"""
    _run(c, "pytest")


@task
def precommit(c):
    """Run pre-commit hooks"""
    _run(c, "pre-commit run --all-files")


@task
def coverage(c):
    """Create coverage report"""
    _run(c, f"coverage run --source {SOURCE_DIR} -m pytest")
    _run(c, "coverage report")

    # Build a local report
    _run(c, "coverage html")
    webbrowser.open(COVERAGE_REPORT.as_uri())


@task
def build_docs(c, preview=False, full=False):
    """Confirm docs can be built"""
    if full:
        if not (ROOT_DIR / "cache" / "lego.blend").exists():
            console.print("File `cache/lego.blend` not found, you can get it by running the command:")
            console.print(
                "gdown https://drive.google.com/file/d/1CQVxGvPLLUYUpkBpATgSd63wgJIzfc6m/view?usp=sharing --fuzzy"
            )
            return

        with c.cd(ROOT_DIR / "cache"):
            # Create examples from the quick start guide
            with open(ROOT_DIR / "examples/quickstart.sh", "r") as f:
                cmds = [line for line in f.readlines() if line.strip() and not line.startswith("#")]

            cmds += [
                f"gifski $(ls -1a quickstart/lego-gt/frames/*.png | sed -n '1~5p') --fps 25 -o {DOCS_STATIC}/lego-gt-preview.gif --width=320 --height=320",
                f"gifski quickstart/lego-rgb25fps/frames/*.png --fps 25 -o {DOCS_STATIC}/lego-rgb25fps-preview.gif --width=320 --height=320",
                f"gifski $(ls -1a quickstart/lego-spc4kHz/frames/*.png | sed -n '1~160p') --fps 25 -o {DOCS_STATIC}/lego-spc4kHz-preview.gif --width=320 --height=320",
                f"gifski $(ls -1a quickstart/lego-dvs125fps/frames/*.png | sed -n '1~5p') --fps 25 -o {DOCS_STATIC}/lego-dvs125fps-preview.gif --width=320 --height=320",
            ]
            for cmd in cmds:
                _run(c, cmd, echo=True, warn=True)

            # Create interpolation examples
            for i, n in enumerate((25, 50, 100, 200)):
                for cmd in (
                    f"visionsim blender.render-animation lego.blend interpolation/lego-{n:04}/ --keyframe-multiplier={n/100} --width=320 --height=320",
                    f"visionsim interpolate.frames interpolation/lego-{n:04}/ -o interpolation/lego{n:04}-interp/ -n={int(64 / 2**i)}",
                    f"gifski $(ls -1a interpolation/lego{n:04}-interp/frames/*.png | sed -n '1~8p') --fps 25 -o {DOCS_STATIC}/lego{n:04}-interp.gif",
                ):
                    _run(c, cmd, echo=True, warn=True)

    # Run autodocs
    with c.cd(ROOT_DIR):
        # TODO: Make this a project configuration
        api_exclude = ["visionsim/interpolate/rife"]
        # We have to do this for all the new changes in the docs to be reflected
        console.print(
            '[yellow]Make sure to run "pip install -e .[dev]" or equivalent to make sure docstring changes are reflected!'
        )
        # Generate API and CLI docs
        _run(c, "sphinx-apidoc -f --remove-old -o docs/source/apidocs visionsim " + " ".join(api_exclude))
        # Move CLI docs to its own folder
        _run(c, "mv docs/source/apidocs/visionsim.cli.rst docs/source/clidocs")

    with c.cd(DOCS_DIR):
        _run(c, "make html")

    if preview:
        webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_build(c):
    """Clean up files from package building"""
    _delete_file("build/")
    _delete_file("dist/")
    _delete_file(".eggs/")
    _delete_pattern("*.egg-info")
    _delete_pattern("*.egg")


@task
def clean_python(c):
    """Clean up python file artifacts"""
    _delete_pattern("__pycache__")
    _delete_pattern("*.pyc")
    _delete_pattern("*.pyo")
    _delete_pattern("*~")


@task
def clean_tests(c):
    """Clean up files from testing"""
    _delete_file(COVERAGE_FILE)
    _delete_file(COVERAGE_DIR)
    _delete_pattern(".pytest_cache")


@task
def clean_docs(c):
    """Clean up docs build"""
    with c.cd(DOCS_DIR):
        _run(c, "make clean")


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(c):
    """Runs all clean sub-tasks"""
    _run(c, "ruff clean")
