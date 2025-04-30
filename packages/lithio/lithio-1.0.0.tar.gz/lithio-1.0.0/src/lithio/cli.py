import os
import shutil
import pwd
import grp
import subprocess
import typer
import hashlib
from pathlib import Path

app = typer.Typer()

# -------- Checksum Verification -------- #
def load_checksums(checksum_file: Path) -> dict[str, str]:
    checksums = {}
    with checksum_file.open() as f:
        for line in f:
            if ':' not in line:
                continue
            name, hash_value = line.strip().split(':', 1)
            checksums[name.strip()] = hash_value.strip()
    return checksums

def compute_checksum(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_checksum(path: Path, expected_hash: str, algo: str):
    actual = compute_checksum(path, algo)
    if actual != expected_hash:
        typer.secho(f"Checksum mismatch: {path.name}", fg=typer.colors.RED)
        typer.secho(f"  Expected: {expected_hash}", fg=typer.colors.RED)
        typer.secho(f"  Actual:   {actual}", fg=typer.colors.RED)
        raise typer.Exit(1)

# -------- Core File Install -------- #
def resolve_user(user: str | None) -> int:
    return pwd.getpwnam(user).pw_uid if user else -1

def resolve_group(group: str | None) -> int:
    return grp.getgrnam(group).gr_gid if group else -1

def set_attributes(path: Path, mode: str | None, owner: str | None, group: str | None):
    if mode:
        path.chmod(int(mode, 8))
    if owner or group:
        uid = resolve_user(owner)
        gid = resolve_group(group)
        os.chown(path, uid, gid)

def strip_binary(path: Path):
    if not path.is_file() or not os.access(path, os.X_OK):
        typer.secho(f"Skipping strip: not executable - {path}", fg=typer.colors.YELLOW)
        return
    subprocess.run(["strip", str(path)], check=True)

def install_file(
    src: Path, dst: Path, mode: str | None, owner: str | None,
    group: str | None, do_strip: bool, preserve: bool,
    mkdir_parents: bool, overwrite: bool, reject_symlinks: bool
):
    if dst.exists():
        if not overwrite:
            typer.secho(f"Error: {dst} exists. Use --overwrite to replace it.", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)
        if reject_symlinks and dst.is_symlink():
            typer.secho(f"Refusing to overwrite symlink: {dst}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    if mkdir_parents:
        dst.parent.mkdir(parents=True, exist_ok=True)

    if preserve:
        shutil.copy2(src, dst)
    else:
        shutil.copy(src, dst)

    if do_strip:
        strip_binary(dst)

    set_attributes(dst, mode, owner, group)

def install_directory(path: Path, mode: str | None, owner: str | None, group: str | None):
    path.mkdir(parents=True, exist_ok=True)
    set_attributes(path, mode, owner, group)

@app.command()
def install(
    files: list[Path] = typer.Argument(..., help="Source files or directories"),
    destination: Path = typer.Argument(..., help="Target file or directory"),
    d: bool = typer.Option(False, "-d", help="Create directories only"),
    D: bool = typer.Option(False, "-D", help="Create leading directories as needed"),
    mode: str = typer.Option(None, "-m", help="Set file permission mode (e.g., 755)"),
    owner: str = typer.Option(None, "-o", help="Set file owner"),
    group: str = typer.Option(None, "-g", help="Set file group"),
    do_strip: bool = typer.Option(False, "--strip", help="Strip binary after copying"),
    preserve: bool = typer.Option(False, "--preserve-timestamps", help="Preserve file timestamps"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Allow overwriting existing files"),
    reject_symlinks: bool = typer.Option(True, "--reject-symlinks/--follow-symlinks", help="Reject overwriting symlinks"),
    checksum: Path = typer.Option(None, "--checksum", help="Path to checksum file with 'filename:hash' lines"),
    checksum_type: str = typer.Option("sha256", "--checksum-type", help="Hash algorithm: md5, sha1, sha256, sha512")
):
    if checksum:
        if checksum_type not in hashlib.algorithms_available:
            typer.secho(f"Invalid checksum type: {checksum_type}", fg=typer.colors.RED)
            raise typer.Exit(1)
        checksum_map = load_checksums(checksum)
        for file in files:
            if file.name not in checksum_map:
                typer.secho(f"No checksum entry for: {file.name}", fg=typer.colors.RED)
                raise typer.Exit(1)
            verify_checksum(file, checksum_map[file.name], checksum_type)

    if d:
        for dir_path in files:
            install_directory(dir_path, mode, owner, group)
        raise typer.Exit()

    if destination.is_dir() or len(files) > 1:
        destination.mkdir(parents=True, exist_ok=True)
        for src in files:
            dst = destination / src.name
            install_file(src, dst, mode, owner, group, do_strip, preserve, D, overwrite, reject_symlinks)
    else:
        install_file(files[0], destination, mode, owner, group, do_strip, preserve, D, overwrite, reject_symlinks)

if __name__ == "__main__":
    app()
