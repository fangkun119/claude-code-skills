"""
Archive a directory into a .tar.gz file.

- If the .tar.gz does not exist: create a new archive from the directory.
- If the .tar.gz already exists: add or update files from the directory
  into the existing archive. Existing files are overwritten with newer
  versions; files already in the archive but no longer on disk are kept.

Usage:
    python archive_dir.py <directory_path>

Example:
    python archive_dir.py ./to_path/target_dir/
    -> creates or updates ./to_path/target_dir.tar.gz
"""

import sys
import os
import tarfile
import tempfile


def collect_disk_files(dir_path: str) -> dict:
    """Collect all files from disk, keyed by archive member name."""
    files = {}
    for root, _, filenames in os.walk(dir_path):
        for fname in filenames:
            full = os.path.join(root, fname)
            member_name = os.path.relpath(full, os.path.dirname(dir_path))
            files[member_name] = full
    return files


def archive_dir(dir_path: str) -> None:
    dir_path = dir_path.rstrip("/")
    if not os.path.isdir(dir_path):
        print(f"[ERROR] '{dir_path}' is not a directory or does not exist.", file=sys.stderr)
        sys.exit(1)

    parent = os.path.dirname(dir_path) or "."
    dirname = os.path.basename(dir_path)
    tar_path = os.path.join(parent, f"{dirname}.tar.gz")

    if not os.path.exists(tar_path):
        print(f"[INFO] Creating new archive: {tar_path}")
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(dir_path, arcname=dirname)
        print(f"[DONE] Created {tar_path}")
        return

    print(f"[INFO] Updating existing archive: {tar_path}")

    disk_files = collect_disk_files(dir_path)
    disk_member_names = set(disk_files.keys())

    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp_path = tmp.name

    added = 0
    updated = 0

    with tarfile.open(tar_path, "r:gz") as old_tar, tarfile.open(tmp_path, "w:gz") as new_tar:
        # Copy existing members; update those that also exist on disk
        for member in old_tar.getmembers():
            if member.name in disk_member_names:
                # File exists on disk: overwrite with disk version
                new_tar.add(disk_files[member.name], arcname=member.name)
                disk_member_names.discard(member.name)
                updated += 1
            else:
                # File only in archive: keep as-is
                f = old_tar.extractfile(member)
                if f:
                    new_tar.addfile(member, f)
                else:
                    new_tar.addfile(member)

        # Add new files from disk that weren't in the archive
        for member_name in disk_member_names:
            new_tar.add(disk_files[member_name], arcname=member_name)
            added += 1

    os.replace(tmp_path, tar_path)
    print(f"[DONE] Updated {tar_path} ({updated} updated, {added} added)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python archive_dir.py <directory_path>", file=sys.stderr)
        sys.exit(1)
    archive_dir(sys.argv[1])
