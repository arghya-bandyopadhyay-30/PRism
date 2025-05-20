import re
from typing import List, Dict, Any
from utils.constants import (
    PYTHON_FILE_EXTENSION, PATCH_KEY, FILE_PATH, FILENAME_KEY, LINE_NUMBER,
    LINE_NUMBER_REGEX, HUNK_HEADER_PREFIX, EMPTY_STRING, ADDED_LINE_PREFIX,
    ADDED_FILE_PREFIX, REMOVED_LINE_PREFIX, CONTENT
)
from utils.logger import get_logger

logger = get_logger(__name__)


class DiffParser:
    """
    Extracts added lines from diff patches of .py files in a PR.
    """
    def __parse_patch(self, file: Dict[str, Any]) -> List[Dict[str, Any]]:
        file_path = file.get(FILENAME_KEY, "")
        if not file_path.endswith(PYTHON_FILE_EXTENSION):
            logger.debug(f"Skipping non-Python file: {file_path}")
            return []

        patch = file.get(PATCH_KEY, "")
        if not patch:
            logger.warning(f"No patch found for file: {file_path}")
            return []

        lines = patch.split("\n")
        results = [
            {
                FILE_PATH: file_path,
                LINE_NUMBER: self.__calculate_line_number(lines, i),
                CONTENT: self.__clean_content(line)
            }
            for i, line in enumerate(lines)
            if self.__is_valid_added_line(line) and self.__clean_content(line).strip()
        ]

        logger.info(f"Parsed {len(results)} added line(s) from: {file_path}")
        return results

    def extract_changed_lines(self, files_json: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extracts all added Python lines from all changed files.
        """
        logger.info(f"Extracting changed lines from {len(files_json)} file(s)...")
        changed_lines = [line for file in files_json for line in self.__parse_patch(file)]
        logger.info(f"Total changed lines extracted: {len(changed_lines)}")
        return changed_lines

    def __is_valid_added_line(self, line: str) -> bool:
        return line.startswith(ADDED_LINE_PREFIX) and not line.startswith(ADDED_FILE_PREFIX)

    def __clean_content(self, line: str) -> str:
        content = line[1:].lstrip()
        return content[2:].lstrip() if content.startswith("- ") else content

    def __calculate_line_number(self, lines: List[str], index: int) -> int:
        hunk_header = next(
            (l for l in lines[:index][::-1] if l.startswith(HUNK_HEADER_PREFIX)), EMPTY_STRING
        )
        match = re.search(LINE_NUMBER_REGEX, hunk_header)
        base = int(match.group(1)) if match else 0
        added_count = sum(
            1 for l in lines[:index]
            if (
                l.startswith(ADDED_LINE_PREFIX) and not l.startswith(ADDED_FILE_PREFIX)
            ) or (
                not l.startswith(REMOVED_LINE_PREFIX) and not l.startswith(HUNK_HEADER_PREFIX)
            )
        )
        return base + added_count
