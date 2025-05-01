import os
import platform
import shutil
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py

# --- Configuration ---
# Path to the CoreOCR Swift project directory (now a submodule within this repo)
SWIFT_PROJECT_DIR = Path(__file__).parent / "CoreOCR"
# Name of the Swift library product
SWIFT_LIBRARY_PRODUCT_NAME = "CoreOCRLib"
# Target path for the dylib within the Python package
TARGET_DYLIB_NAME = f"lib{SWIFT_LIBRARY_PRODUCT_NAME}.dylib"
PACKAGE_NAME = "pyCoreOCR" # Matches the directory name and pyproject.toml

class CustomBuildPy(build_py):
    """Custom build command to build Swift library and include the dylib."""

    def run(self):
        # --- Check Prerequisites ---
        if platform.system() != "Darwin":
            raise OSError("This package requires macOS to build the Swift library.")

        if not shutil.which("swift"):
            raise OSError(
                "Swift compiler not found. Please install Xcode command line tools "
                "or the Swift toolchain."
            )

        swift_project_path = SWIFT_PROJECT_DIR.resolve()
        if not (swift_project_path / "Package.swift").is_file():
             raise FileNotFoundError(
                 f"Swift project not found at expected location: {swift_project_path}"
             )

        print("-" * 20)
        print(f"Building Swift library: {SWIFT_LIBRARY_PRODUCT_NAME}")
        print(f"Swift project directory: {swift_project_path}")
        print("-" * 20)

        # --- Build Swift Library ---
        try:
            # Build for release, targeting the specific library product
            subprocess.run(
                [
                    "swift", "build",
                    "-c", "release",
                    "--product", SWIFT_LIBRARY_PRODUCT_NAME,
                    # "--disable-sandbox", # May be needed in some environments
                ],
                cwd=swift_project_path,
                check=True,
                capture_output=True, # Capture output
                text=True          # Decode output as text
            )
            print("Swift build successful.")
        except subprocess.CalledProcessError as e:
            print("--- Swift Build Failed ---")
            print("Command:", " ".join(e.cmd))
            print("Return Code:", e.returncode)
            print("--- stdout ---")
            print(e.stdout)
            print("--- stderr ---")
            print(e.stderr)
            print("-------------------------")
            # Re-raise a more informative error
            raise RuntimeError("Swift build failed.") from e
        except FileNotFoundError:
             raise FileNotFoundError("`swift` command not found.")

        # --- Find and Copy Dylib ---
        # Default path for release build artifacts
        swift_build_dir = swift_project_path / ".build" / "release"
        source_dylib_path = swift_build_dir / TARGET_DYLIB_NAME

        if not source_dylib_path.is_file():
            raise FileNotFoundError(
                f"Built Swift library not found at expected location: {source_dylib_path}"
            )

        # Destination directory within the source package itself
        # Path(__file__).parent gives the dir of setup.py (pyCoreOCR)
        package_source_dir = Path(__file__).parent / PACKAGE_NAME
        package_source_dir.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        target_dylib_path = package_source_dir / TARGET_DYLIB_NAME

        # Delete existing dylib first to avoid potential issues (e.g., if it was a symlink)
        if target_dylib_path.exists():
             print(f"Removing existing target: {target_dylib_path}")
             target_dylib_path.unlink()
        elif target_dylib_path.is_symlink(): # Check for broken symlinks too
             print(f"Removing existing broken symlink: {target_dylib_path}")
             target_dylib_path.unlink()

        print(f"Copying {source_dylib_path} to {target_dylib_path}")
        shutil.copyfile(source_dylib_path, target_dylib_path)
        # Make the copied dylib executable
        os.chmod(target_dylib_path, 0o755)

        # --- Run Original Build ---
        super().run()


# Use setup() even with pyproject.toml for custom build steps
setup(
    # name, version, etc. are defined in pyproject.toml
    # We only need setup.py for the custom build logic
    cmdclass={
        'build_py': CustomBuildPy,
    },
    # Ensure the .dylib is included in the package data
    # The path is relative to the package directory (pyCoreOCR/pyCoreOCR)
    package_data={
        PACKAGE_NAME: [TARGET_DYLIB_NAME],
    },
    # This is important for setuptools to know the package includes non-Python data
    zip_safe=False,
) 