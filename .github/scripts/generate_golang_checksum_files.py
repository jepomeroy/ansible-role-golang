"""
Generate YAML files containing SHA256 checksums for Go redistributable packages.

This script fetches Go version information from the official Go API and generates
YAML variable files for each stable version and architecture combination. These
files are used by the Ansible role to verify the integrity of downloaded Go packages.
"""

from typing import List

import requests

# Define the API endpoint URL for fetching Go version metadata
url = "https://go.dev/dl/?mode=json&include=all"


class File:
    """
    Represents a Go redistributable file with its metadata.

    This class encapsulates information about a specific Go package file,
    including its filename, architecture, and SHA256 checksum.
    """

    def __init__(self, file: dict):
        """
        Initialize a File instance from API response data.

        Args:
            file: Dictionary containing file metadata from the Go API,
                  including 'filename', 'arch', and 'sha256' keys.
        """
        self._filename = file["filename"]
        self._arch = file["arch"]
        self._sha256 = file["sha256"]

    def __str__(self) -> str:
        """Return a formatted string representation of the file metadata."""
        return (
            f"\tsha256: {self._sha256}, arch: {self._arch}, "
            f"filename: {self._filename}\n"
        )

    @property
    def filename(self) -> str:
        """Get the filename of the Go redistributable package."""
        return self._filename

    @property
    def arch(self) -> str:
        """Get the architecture of the package (e.g., amd64, arm64, armv6l)."""
        return self._arch

    @property
    def sha256(self) -> str:
        """Get the SHA256 checksum of the package."""
        return self._sha256


class Version:
    """
    Represents a Go version with its associated redistributable files.

    This class encapsulates a specific Go version and all its available
    Linux package files for supported architectures.
    """

    def __init__(self, version: dict):
        """
        Initialize a Version instance from API response data.

        Args:
            version: Dictionary containing version metadata from the Go API,
                     including 'version' string and 'files' list.
                     The version string has 'go' prefix removed (e.g., '1.21.0').
        """
        # Remove 'go' prefix from version string (e.g., 'go1.21.0' -> '1.21.0')
        self._version = version["version"][2:]
        self._files = make_files(version["files"])

    def __str__(self) -> str:
        """Return a formatted string representation of the version and its files."""
        s = f"version: {self._version}\n"
        for f in self._files:
            s += f"{f}"

        return s

    @property
    def version(self) -> str:
        """Get the version string (without 'go' prefix, e.g., '1.21.0')."""
        return self._version

    @property
    def files(self) -> List[File]:
        """Get the list of File objects for this version."""
        return self._files


def get_versions(url: str) -> dict | None:
    """
    Fetch Go version information from the official Go API.

    Args:
        url: The API endpoint URL to fetch version data from.

    Returns:
        A dictionary containing version metadata if successful, None otherwise.
        The dictionary includes information about all Go versions and their files.

    Raises:
        No exceptions are raised; errors are handled internally and None is returned.
    """
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions (timeout, connection errors, etc.)
        print(f"Error: {e}")
        return None


def make_files(files: list[dict]) -> list[File]:
    """
    Filter and create File objects for supported Linux architectures.

    This function processes the files list from the API response and creates
    File objects only for Linux packages with supported architectures.

    Args:
        files: List of dictionaries containing file metadata from the API.

    Returns:
        A list of File objects for Linux packages with amd64, arm64, or armv6l architecture.
    """
    f_arr = []

    # Only include Linux packages for supported architectures
    for file in files:
        if file["os"] == "linux" and file["arch"] in ["amd64", "arm64", "armv6l"]:
            f_arr.append(File(file))

    return f_arr


def make_versions(versions: dict) -> list[Version]:
    """
    Filter and create Version objects for stable Go releases.

    This function processes the API response and creates Version objects
    only for stable releases, excluding the special 'go1' version.

    Args:
        versions: Dictionary containing all version data from the Go API.

    Returns:
        A list of Version objects for stable Go releases (excluding 'go1').
    """
    vers = []

    # Only include stable versions, excluding the special 'go1' version
    for version in versions:
        if version["stable"] is True and version["version"] != "go1":
            ver = Version(version)
            vers.append(ver)

    return vers


def write_files(root: str, versions: list[Version]) -> None:
    """
    Write YAML files containing SHA256 checksums for each version and architecture.

    This function creates YAML variable files in the specified directory,
    with one file per version-architecture combination. Each file contains
    the SHA256 checksum for verifying the integrity of the Go package.

    Args:
        root: The root directory path where YAML files will be written.
        versions: List of Version objects to process.

    File naming format: {version}-{arch}.yml (e.g., '1.21.0-amd64.yml')
    """
    for version in versions:
        for file in version.files:
            # Only write files if SHA256 checksum is available
            if file.sha256 is not None:
                filename = f"{root}/{version.version}-{file.arch}.yml"
                with open(filename, "w") as f:
                    # Write YAML header
                    f.write("---\n")
                    # Add comment indicating which package this checksum is for
                    comment = (
                        f"# SHA256 sum for the redistributable "
                        f"package {file.filename}\n"
                    )
                    f.write(comment)
                    # Write the Ansible variable with the checksum
                    f.write(f"golang_redis_sha256sum: '{file.sha256}'\n")


def main() -> None:
    """
    Main entry point for the script.

    This function orchestrates the entire process:
    1. Fetches Go version data from the API
    2. Filters for stable versions
    3. Writes YAML checksum files to ./vars/versions/

    The generated files are used by the Ansible role to verify downloaded packages.
    """
    response = get_versions(url)

    if response is not None:
        # Parse the API response and filter for stable versions
        versions = make_versions(response)

        # Write YAML files with checksums to the vars/versions directory
        write_files("./vars/versions", versions)


if __name__ == "__main__":
    main()
