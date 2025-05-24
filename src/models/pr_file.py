from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class PRFile:
    filename: str
    status: str
    patch: Optional[str] = ""
    raw_url: Optional[str] = ""
    deletions: Optional[int] = 0
    changes: Optional[int] = 0
    additions: Optional[int] = 0
    blob_url: Optional[str] = ""
    contents_url: Optional[str] = ""
    sha: Optional[str] = ""

    @classmethod
    def from_dict(cls, file_dict: Dict) -> "PRFile":
        if "filename" not in file_dict:
            raise ValueError("Missing 'filename' in file_dict")
        if "status" not in file_dict:
            raise ValueError("Missing 'status' in file_dict")

        return cls(
            filename=file_dict["filename"],
            status=file_dict["status"],
            patch=file_dict.get("patch", ""),
            raw_url=file_dict.get("raw_url", ""),
            deletions=file_dict.get("deletions", 0),
            changes=file_dict.get("changes", 0),
            additions=file_dict.get("additions", 0),
            blob_url=file_dict.get("blob_url", ""),
            contents_url=file_dict.get("contents_url", ""),
            sha=file_dict.get("sha", "")
        )

    def to_dict(self) -> Dict:
        return {
            "filename": self.filename,
            "status": self.status,
            "patch": self.patch,
            "raw_url": self.raw_url,
            "deletions": self.deletions,
            "changes": self.changes,
            "additions": self.additions,
            "blob_url": self.blob_url,
            "contents_url": self.contents_url,
            "sha": self.sha
        }
