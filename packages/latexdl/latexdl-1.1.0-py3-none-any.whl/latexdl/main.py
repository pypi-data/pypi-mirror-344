from __future__ import annotations

import argparse
import contextlib
import logging
import re
import shutil
import tarfile
import tempfile
import urllib.parse
from pathlib import Path

import requests
from tqdm import tqdm

from ._bibtex import detect_and_collect_bibtex
from .expand import expand_latex_file
from .strip import check_pandoc_installed, strip


def _extract_arxiv_id(package: str) -> str:
    # Approved formats (square brackets denote optional parts):
    # - arXiv ID (e.g., 2103.12345[v#])
    # - Full PDF URL (e.g., https://arxiv.org/pdf/2103.12345[v#][.pdf])
    # - Full Abs URL (e.g., https://arxiv.org/abs/2103.12345[v#])

    if package.startswith("http"):
        # Full URL
        if "pdf" in package:
            # Full PDF URL
            arxiv_id = Path(urllib.parse.urlparse(package).path).name
            if arxiv_id.endswith(".pdf"):
                arxiv_id = arxiv_id[: -len(".pdf")]
        elif "abs" in package:
            # Full Abs URL
            arxiv_id = Path(urllib.parse.urlparse(package).path).name
        else:
            raise ValueError(f"Invalid package URL format: {package}")
    else:
        # arXiv ID
        arxiv_id = package

    return arxiv_id


def _download_and_extract(
    arxiv_id: str,
    output: Path,
    redownload_existing: bool = False,
):
    fpath = output / f"{arxiv_id}.tar.gz"
    if fpath.exists() and not redownload_existing:
        logging.info(f"Package {arxiv_id} already downloaded, skipping")
        return

    url = f"https://arxiv.org/src/{arxiv_id}"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Save the response to a file
    with fpath.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract the tarball
    with tarfile.open(fpath, "r:gz") as tar:
        tar.extractall(output)


def _find_main_latex_file(directory: Path) -> Path | None:
    potential_main_files: list[tuple[Path, float]] = []

    for file_path in directory.rglob("*.[tT][eE][xX]"):  # Case insensitive extension
        score = 0.0

        # Check filename
        if file_path.name.lower() in ["main.tex", "paper.tex", "article.tex"]:
            score += 5

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except UnicodeDecodeError:
            # Skip files that can't be read as UTF-8
            continue

        # Check for \documentclass
        if r"\documentclass" in content:
            score += 3

        # Check for document environment
        if r"\begin{document}" in content and r"\end{document}" in content:
            score += 4

        # Check for multiple \input or \include commands
        if len(re.findall(r"\\(input|include)", content)) > 1:
            score += 2

        # Check for bibliography
        if r"\bibliography" in content or r"\begin{thebibliography}" in content:
            score += 2

        # Consider file size
        score += min(file_path.stat().st_size / 1000, 5)  # Max 5 points for size

        potential_main_files.append((file_path, score))

    # Sort by score in descending order
    potential_main_files.sort(key=lambda x: x[1], reverse=True)

    return potential_main_files[0][0] if potential_main_files else None


def process_packages(
    packages: list[str],
    output_directory: Path | None = None,
    markdown: bool | None = None,
    redownload_existing: bool = False,
    force_overwrite: bool = False,
    keep_comments: bool = False,
    bib: bool = True,
    progress_bar: bool = True,
) -> dict[str, str | Path]:
    """
    Process arXiv packages to download and convert LaTeX files.

    Args:
        packages: list of arXiv IDs or URLs
        output_directory: Directory to save the files (None for in-memory output)
        markdown: Whether to convert to markdown (None to auto-detect based on pandoc)
        redownload_existing: Whether to redownload existing packages
        force_overwrite: Whether to overwrite existing directories without prompting
        keep_comments: Whether to keep comments in the expanded LaTeX
        bib: Whether to include bibliography content
        progress_bar: Whether to display a progress bar

    Returns:
        Dictionary mapping arXiv IDs to either file paths (if output_directory is provided)
        or content strings (if output_directory is None)
    """
    # If markdown is not set, check if pandoc is installed
    if markdown is None:
        markdown = check_pandoc_installed()
        logging.info(
            f"Using {'markdown' if markdown else 'LaTeX'} output format (pandoc is {'installed' if markdown else 'not installed'})"
        )

    output_base: Path | None = output_directory
    output_stdout = output_base is None
    results = {}

    with contextlib.ExitStack() as stack:
        if output_base is None:
            output_base = Path(stack.enter_context(tempfile.TemporaryDirectory()))

        # Resolve the packages
        arxiv_ids: list[str] = []
        for package in packages:
            assert isinstance(package, str), "Package must be a string"
            arxiv_ids.append(_extract_arxiv_id(package))

        # Process the packages
        iterator = arxiv_ids
        pbar = None
        if progress_bar:
            iterator = pbar = tqdm(arxiv_ids)
        for arxiv_id in iterator:
            output = output_base / arxiv_id

            # If the package dir exists, handle according to force_overwrite
            if output.exists():
                logging.info(f"Output path {output} already exists")
                if not output.is_dir():
                    raise ValueError(f"Output path {output} is not a directory")

                if force_overwrite:
                    # Remove the directory
                    logging.warning(
                        f"Removing {output} because of force_overwrite=True"
                    )
                    shutil.rmtree(output)
                else:
                    # In programmatic mode, we skip instead of asking for input
                    if not output_stdout:
                        logging.warning(
                            f"Skipping {arxiv_id} (directory exists and force_overwrite=False)"
                        )
                        continue
                    else:
                        # For stdout mode, we can still process
                        pass

            # Create the directory
            output.mkdir(parents=True, exist_ok=True)

            # Download and extract the package
            if pbar is not None:
                pbar.set_description(f"Downloading {arxiv_id}")
            try:
                _download_and_extract(
                    arxiv_id, output, redownload_existing=redownload_existing
                )
            except IOError:
                logging.error(f"Error downloading/extracting {arxiv_id}", exc_info=True)
                continue

            # Find the main LaTeX file in the extracted directory
            if (main_file := _find_main_latex_file(output)) is None:
                logging.error(
                    f"Could not find the main LaTeX for ID {arxiv_id} (output: {output})"
                )
                continue

            logging.info(f"Resolved main LaTeX file: {main_file}")

            try:
                if pbar:
                    pbar.set_description(f"Processing {arxiv_id} latex")

                # Expand the LaTeX file (i.e., resolve imports into 1 large file)
                expanded_latex = expand_latex_file(
                    main_file, keep_comments=keep_comments
                )

                # Convert to text if requested
                if markdown:
                    expanded = strip(expanded_latex)
                else:
                    expanded = expanded_latex

                # Add bibliography content if requested
                if bib and (
                    bib_content := detect_and_collect_bibtex(
                        output,
                        expanded_latex,
                        markdown=markdown,
                    )
                ):
                    if markdown:
                        expanded += f"\n\n# References\n\n{bib_content}"
                    else:
                        expanded += f"\n\nREFERENCES\n\n{bib_content}"

                # Store results based on output mode
                if output_stdout:
                    results[arxiv_id] = expanded
                else:
                    extension = "md" if markdown else "tex"
                    output_file_path = output_base / f"{arxiv_id}.{extension}"
                    if pbar:
                        pbar.set_description(
                            f"Writing {arxiv_id} to {output_file_path}"
                        )
                    with output_file_path.open("w", encoding="utf-8") as f:
                        f.write(expanded)
                    results[arxiv_id] = output_file_path

            except IOError:
                logging.error(f"Error converting {arxiv_id}", exc_info=True)
                continue

    return results


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Download LaTeX packages")
    parser.add_argument("packages", nargs="+", help="Packages to download", type=str)
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--markdown",
        help="Use pandoc to convert to markdown",
        action=argparse.BooleanOptionalAction,
        required=False,
    )
    parser.add_argument(
        "--redownload-existing",
        help="Redownload existing packages",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--force-overwrite",
        help="Force overwrite of existing files",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--keep-comments",
        help="Keep comments in the expanded LaTeX file",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--bib",
        help="Include bibliography file content",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    args = parser.parse_args()

    # Call the process_packages function with command-line arguments
    results = process_packages(
        packages=args.packages,
        output_directory=args.output,
        markdown=args.markdown,
        redownload_existing=args.redownload_existing,
        force_overwrite=args.force_overwrite,
        keep_comments=args.keep_comments,
        bib=args.bib,
    )

    # Print to stdout if no output directory was specified
    if args.output is None:
        for arxiv_id, content in results.items():
            print(content)


if __name__ == "__main__":
    main()
