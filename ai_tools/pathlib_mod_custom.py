from __future__ import annotations
import pathlib
Path = pathlib.Path
PurePath = pathlib.PurePath
import atexit
import contextlib
import fnmatch
import importlib.util
import itertools
import logging
import os
import shutil
import sys
import types
import uuid
from enum import Enum
from collections.abc import Callable, Iterable, Iterator
from errno import EBADF, ELOOP, ENOENT, ENOTDIR
from functools import partial
from importlib.machinery import ModuleSpec, PathFinder
from os.path import expanduser, expandvars, isabs, sep
from pathlib import Path, PurePath
from posixpath import sep as posix_sep
from typing import Any, TypeVar

try:
    import stat_mod
except ImportError:
    import stat as stat_mod  # fallback to stdlib if custom not present

import pathlib
Path = pathlib.Path
PurePath = pathlib.PurePath

# Optional pytest compatibility
try:
    from _pytest.compat import assert_never
    from _pytest.outcomes import skip
    from _pytest.warning_types import PytestWarning
except ImportError:
    def assert_never(value): raise AssertionError(f"Unexpected value: {value}")
    def skip(msg): raise NotImplementedError("Skip not available")
    class PytestWarning(Warning): pass

if sys.version_info < (3, 11):
    from importlib._bootstrap_external import _NamespaceLoader as NamespaceLoader
else:
    from importlib.machinery import NamespaceLoader

LOCK_TIMEOUT = 60 * 60 * 24 * 3

_AnyPurePath = TypeVar("_AnyPurePath", bound=PurePath)

_IGNORED_ERRORS = (ENOENT, ENOTDIR, EBADF, ELOOP)
_IGNORED_WINERRORS = (
    21,   # ERROR_NOT_READY - drive exists but is not accessible
    1921, # ERROR_CANT_RESOLVE_FILENAME - fix for broken symlink pointing to itself
)

logger = logging.getLogger("pathlib_mod")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def _ignore_error(exception: Exception) -> bool:
    """Return True if the exception is ignorable."""
    return (
        getattr(exception, "errno", None) in _IGNORED_ERRORS
        or getattr(exception, "winerror", None) in _IGNORED_WINERRORS
    )


def get_lock_path(path: _AnyPurePath) -> _AnyPurePath:
    """Return lock file path for given directory or file."""
    return path.joinpath(".lock")


def on_rm_rf_error(
    func: Callable[..., Any] | None,
    path: str,
    excinfo: BaseException | tuple[type[BaseException], BaseException, types.TracebackType | None],
    *,
    start_path: Path,
) -> bool:
    """
    Handle known read-only errors during rmtree.
    """
    if isinstance(excinfo, BaseException):
        exc = excinfo
    else:
        exc = excinfo[1]

    if isinstance(exc, FileNotFoundError):
        return False

    if not isinstance(exc, PermissionError):
        logger.warning(f"(rm_rf) error removing {path}\n{type(exc)}: {exc}")
        return False

    if func not in (os.rmdir, os.remove, os.unlink, os.open):
        logger.warning(f"(rm_rf) unknown function {func} when removing {path}:\n{type(exc)}: {exc}")
        return False

    # Chmod + retry.
    def chmod_rw(p: str) -> None:
        try:
            mode = os.stat(p).st_mode
            os.chmod(p, mode | stat_mod.S_IRUSR | stat_mod.S_IWUSR)
        except Exception as e:
            logger.error(f"chmod_rw failed for {p}: {e}")

    p = Path(path)
    if p.is_file():
        for parent in p.parents:
            chmod_rw(str(parent))
            if parent == start_path:
                break
    chmod_rw(str(path))

    try:
        func(path)
    except Exception as e:
        logger.error(f"Failed to remove {path} after chmod: {e}")
        return False
    return True


def ensure_extended_length_path(path: Path) -> Path:
    """
    Return the extended-length version of a path (Windows), else return path unchanged.
    """
    if sys.platform.startswith("win32"):
        path = path.resolve()
        path = Path(get_extended_length_path_str(str(path)))
    return path


def get_extended_length_path_str(path: str) -> str:
    """Convert a path to a Windows extended length path."""
    long_path_prefix = "\\\\?\\"
    unc_long_path_prefix = "\\\\?\\UNC\\"
    if path.startswith((long_path_prefix, unc_long_path_prefix)):
        return path
    if path.startswith("\\\\"):
        return unc_long_path_prefix + path[2:]
    return long_path_prefix + path


def rm_rf(path: Path) -> None:
    """
    Remove the path contents recursively, even if some elements are read-only.
    """
    path = ensure_extended_length_path(path)
    onerror = partial(on_rm_rf_error, start_path=path)
    if sys.version_info >= (3, 12):
        shutil.rmtree(str(path), onexc=onerror)
    else:
        shutil.rmtree(str(path), onerror=onerror)


def find_prefixed(root: Path, prefix: str) -> Iterator[os.DirEntry[str]]:
    """Yield DirEntry objects in root that begin with prefix (case-insensitive)."""
    l_prefix = prefix.lower()
    for x in os.scandir(root):
        if x.name.lower().startswith(l_prefix):
            yield x


def extract_suffixes(iterable: Iterable[os.DirEntry[str]], prefix: str) -> Iterator[str]:
    """Yield suffixes of names after the provided prefix."""
    p_len = len(prefix)
    for entry in iterable:
        yield entry.name[p_len:]


def find_suffixes(root: Path, prefix: str) -> Iterator[str]:
    """Combine find_prefixed and extract_suffixes for convenience."""
    return extract_suffixes(find_prefixed(root, prefix), prefix)


def parse_num(maybe_num: str) -> int:
    """Parse an int from a string, returning -1 on failure."""
    try:
        return int(maybe_num)
    except ValueError:
        return -1


def _force_symlink(root: Path, target: str | PurePath, link_to: str | Path) -> None:
    """Create or update a symlink named target -> link_to in root."""
    current_symlink = root.joinpath(target)
    try:
        current_symlink.unlink()
    except OSError:
        pass
    try:
        current_symlink.symlink_to(link_to)
    except Exception as e:
        logger.warning(f"symlink_to failed: {e}")


def make_numbered_dir(root: Path, prefix: str, mode: int = 0o700) -> Path:
    """
    Create a directory with an incremented numeric suffix for the given prefix.
    """
    for _ in range(10):
        max_existing = max(map(parse_num, find_suffixes(root, prefix)), default=-1)
        new_number = max_existing + 1
        new_path = root.joinpath(f"{prefix}{new_number}")
        try:
            new_path.mkdir(mode=mode)
        except Exception as e:
            logger.info(f"Attempt to create {new_path} failed: {e}")
        else:
            _force_symlink(root, prefix + "current", new_path)
            return new_path
    raise OSError(
        f"could not create numbered dir with prefix {prefix} in {root} after 10 tries"
    )


def create_cleanup_lock(p: Path) -> Path:
    """
    Create a lock to prevent premature folder cleanup.
    """
    lock_path = get_lock_path(p)
    try:
        fd = os.open(str(lock_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError as e:
        raise OSError(f"cannot create lockfile in {p}") from e
    else:
        pid = os.getpid()
        spid = str(pid).encode()
        os.write(fd, spid)
        os.close(fd)
        if not lock_path.is_file():
            raise OSError("lock path got renamed after successful creation")
        return lock_path


def register_cleanup_lock_removal(
    lock_path: Path, register: Any = atexit.register
) -> Any:
    """
    Register a cleanup function for removing a lock, by default on atexit.
    """
    pid = os.getpid()

    def cleanup_on_exit(lock_path: Path = lock_path, original_pid: int = pid) -> None:
        current_pid = os.getpid()
        if current_pid != original_pid:
            return
        try:
            lock_path.unlink()
        except OSError:
            pass

    return register(cleanup_on_exit)


def maybe_delete_a_numbered_dir(path: Path) -> None:
    """
    Remove a numbered directory if its lock can be obtained and it does not seem to be in use.
    """
    path = ensure_extended_length_path(path)
    lock_path = None
    try:
        lock_path = create_cleanup_lock(path)
        parent = path.parent
        garbage = parent.joinpath(f"garbage-{uuid.uuid4()}")
        path.rename(garbage)
        rm_rf(garbage)
    except OSError as e:
        logger.info(f"maybe_delete_a_numbered_dir: {e}")
        return
    finally:
        if lock_path is not None:
            try:
                lock_path.unlink()
            except OSError:
                pass


def ensure_deletable(path: Path, consider_lock_dead_if_created_before: float) -> bool:
    """
    Check if `path` is deletable based on whether the lock file is expired.
    """
    if path.is_symlink():
        return False
    lock = get_lock_path(path)
    try:
        if not lock.is_file():
            return True
    except OSError:
        return False
    try:
        lock_time = lock.stat().st_mtime
    except Exception:
        return False
    else:
        if lock_time < consider_lock_dead_if_created_before:
            with contextlib.suppress(OSError):
                lock.unlink()
                return True
        return False


def try_cleanup(path: Path, consider_lock_dead_if_created_before: float) -> None:
    """
    Try to cleanup a folder if we can ensure it's deletable.
    """
    if ensure_deletable(path, consider_lock_dead_if_created_before):
        maybe_delete_a_numbered_dir(path)


def cleanup_candidates(root: Path, prefix: str, keep: int) -> Iterator[Path]:
    """
    List candidates for numbered directories to be removed - follows py.path.
    """
    max_existing = max(map(parse_num, find_suffixes(root, prefix)), default=-1)
    max_delete = max_existing - keep
    entries = find_prefixed(root, prefix)
    entries, entries2 = itertools.tee(entries)
    numbers = map(parse_num, extract_suffixes(entries2, prefix))
    for entry, number in zip(entries, numbers):
        if number <= max_delete:
            yield Path(entry)


def cleanup_dead_symlinks(root: Path) -> None:
    """Remove dead symlinks in root."""
    for left_dir in root.iterdir():
        if left_dir.is_symlink() and not left_dir.resolve().exists():
            left_dir.unlink()


def cleanup_numbered_dir(
    root: Path, prefix: str, keep: int, consider_lock_dead_if_created_before: float
) -> None:
    """
    Cleanup for lock-driven numbered directories. Keeps 'keep' directories.
    """
    if not root.exists():
        return
    for path in cleanup_candidates(root, prefix, keep):
        try_cleanup(path, consider_lock_dead_if_created_before)
    for path in root.glob("garbage-*"):
        try_cleanup(path, consider_lock_dead_if_created_before)
    cleanup_dead_symlinks(root)


def make_numbered_dir_with_cleanup(
    root: Path,
    prefix: str,
    keep: int,
    lock_timeout: float,
    mode: int,
) -> Path:
    """
    Create a numbered dir with a cleanup lock and remove old ones.
    """
    e = None
    for _ in range(10):
        try:
            p = make_numbered_dir(root, prefix, mode)
            if keep != 0:
                lock_path = create_cleanup_lock(p)
                register_cleanup_lock_removal(lock_path)
        except Exception as exc:
            e = exc
        else:
            consider_lock_dead_if_created_before = p.stat().st_mtime - lock_timeout
            atexit.register(
                cleanup_numbered_dir,
                root,
                prefix,
                keep,
                consider_lock_dead_if_created_before,
            )
            return p
    assert e is not None
    raise e


def resolve_from_str(input: str, rootpath: Path) -> Path:
    """
    Expand user and vars in input and make absolute if needed.
    """
    input = expanduser(input)
    input = expandvars(input)
    if isabs(input):
        return Path(input)
    else:
        return rootpath.joinpath(input)


def fnmatch_ex(pattern: str, path: str | os.PathLike[str]) -> bool:
    """
    A port of FNMatcher from py.path.common which works with PurePath() instances.
    """
    path = PurePath(path)
    iswin32 = sys.platform.startswith("win")
    if iswin32 and sep not in pattern and posix_sep in pattern:
        pattern = pattern.replace(posix_sep, sep)
    if sep not in pattern:
        name = path.name
    else:
        name = str(path)
        if path.is_absolute() and not os.path.isabs(pattern):
            pattern = f"*{os.sep}{pattern}"
    return fnmatch.fnmatch(name, pattern)


def parts(s: str) -> set[str]:
    """Return all path prefixes from a string path."""
    components = s.split(sep)
    return {sep.join(components[:i + 1]) or sep for i in range(len(components))}


def symlink_or_skip(
    src: os.PathLike[str] | str,
    dst: os.PathLike[str] | str,
    **kwargs: Any,
) -> None:
    """
    Make a symlink, or skip if symlinks are not supported.
    """
    try:
        os.symlink(src, dst, **kwargs)
    except OSError as e:
        skip(f"symlinks not supported: {e}")


class ImportMode(Enum):
    """Possible values for `mode` parameter of `import_path`."""
    prepend = "prepend"
    append = "append"
    importlib = "importlib"


class ImportPathMismatchError(ImportError):
    """Raised on import_path() if there is a mismatch of __file__'s."""


def import_path(
    path: str | os.PathLike[str],
    *,
    mode: str | ImportMode = ImportMode.prepend,
    root: Path,
    consider_namespace_packages: bool,
) -> types.ModuleType:
    """
    Import and return a module from the given path, using the specified import mode.
    """
    path = Path(path)
    mode = ImportMode(mode)

    if not path.exists():
        raise ImportError(path)

    if mode is ImportMode.importlib:
        try:
            pkg_root, module_name = resolve_pkg_root_and_module_name(
                path, consider_namespace_packages=consider_namespace_packages
            )
        except CouldNotResolvePathError:
            pass
        else:
            with contextlib.suppress(KeyError):
                return sys.modules[module_name]

            mod = _import_module_using_spec(
                module_name, path, pkg_root, insert_modules=False
            )
            if mod is not None:
                return mod

        module_name = module_name_from_path(path, root)
        with contextlib.suppress(KeyError):
            return sys.modules[module_name]

        mod = _import_module_using_spec(
            module_name, path, path.parent, insert_modules=True
        )
        if mod is None:
            raise ImportError(f"Can't find module {module_name} at location {path}")
        return mod

    try:
        pkg_root, module_name = resolve_pkg_root_and_module_name(
            path, consider_namespace_packages=consider_namespace_packages
        )
    except CouldNotResolvePathError:
        pkg_root, module_name = path.parent, path.stem

    if mode is ImportMode.append:
        if str(pkg_root) not in sys.path:
            sys.path.append(str(pkg_root))
    elif mode is ImportMode.prepend:
        if str(pkg_root) != sys.path[0]:
            sys.path.insert(0, str(pkg_root))
    else:
        assert_never(mode)

    importlib.import_module(module_name)

    mod = sys.modules[module_name]
    if path.name == "__init__.py":
        return mod

    ignore = os.environ.get("PY_IGNORE_IMPORTMISMATCH", "")
    if ignore != "1":
        module_file = mod.__file__
        if module_file is None:
            raise ImportPathMismatchError(module_name, module_file, path)

        if module_file.endswith((".pyc", ".pyo")):
            module_file = module_file[:-1]
        if module_file.endswith(os.sep + "__init__.py"):
            module_file = module_file[:-(len(os.sep + "__init__.py"))]

        try:
            is_same = _is_same(str(path), module_file)
        except FileNotFoundError:
            is_same = False

        if not is_same:
            raise ImportPathMismatchError(module_name, module_file, path)

    return mod


def _import_module_using_spec(
    module_name: str, module_path: Path, module_location: Path, *, insert_modules: bool
) -> types.ModuleType | None:
    """
    Import a module by its canonical name, path, and parent location.
    """
    parent_module_name, _, name = module_name.rpartition(".")
    parent_module: types.ModuleType | None = None
    if parent_module_name:
        parent_module = sys.modules.get(parent_module_name)
        need_reimport = not hasattr(parent_module, "__path__")
        if parent_module is None or need_reimport:
            if module_path.name == "__init__.py":
                parent_module_path = module_path.parent.parent
            else:
                parent_module_path = module_path.parent

            if (parent_module_path / "__init__.py").is_file():
                parent_module_path = parent_module_path / "__init__.py"

            parent_module = _import_module_using_spec(
                parent_module_name,
                parent_module_path,
                parent_module_path.parent,
                insert_modules=insert_modules,
            )

    for meta_importer in sys.meta_path:
        module_name_of_meta = getattr(meta_importer.__class__, "__module__", "")
        if module_name_of_meta == "_pytest.assertion.rewrite" and module_path.is_file():
            find_spec_path = [str(module_location), str(module_path)]
        else:
            find_spec_path = [str(module_location)]

        spec = meta_importer.find_spec(module_name, find_spec_path)
        if spec_matches_module_path(spec, module_path):
            break
    else:
        loader = None
        if module_path.is_dir():
            loader = NamespaceLoader(name, module_path, PathFinder())  # type: ignore[arg-type]

        spec = importlib.util.spec_from_file_location(
            module_name, str(module_path), loader=loader
        )

    if spec_matches_module_path(spec, module_path):
        assert spec is not None
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)  # type: ignore[union-attr]

        if parent_module is not None:
            setattr(parent_module, name, mod)

        if insert_modules:
            insert_missing_modules(sys.modules, module_name)
        return mod

    return None


def spec_matches_module_path(module_spec: ModuleSpec | None, module_path: Path) -> bool:
    """
    Return true if the given ModuleSpec can be used to import the given module path.
    """
    if module_spec is None:
        return False
    if module_spec.origin:
        return Path(module_spec.origin) == module_path
    if module_spec.submodule_search_locations:
        for path in module_spec.submodule_search_locations:
            if Path(path) == module_path:
                return True
    return False


if sys.platform.startswith("win"):
    def _is_same(f1: str, f2: str) -> bool:
        return Path(f1) == Path(f2) or os.path.samefile(f1, f2)
else:
    def _is_same(f1: str, f2: str) -> bool:
        return os.path.samefile(f1, f2)


def module_name_from_path(path: Path, root: Path) -> str:
    """
    Return a dotted module name based on the given path, anchored on root.
    """
    path = path.with_suffix("")
    try:
        relative_path = path.relative_to(root)
    except ValueError:
        path_parts = path.parts[1:]
    else:
        path_parts = relative_path.parts

    if len(path_parts) >= 2 and path_parts[-1] == "__init__":
        path_parts = path_parts[:-1]

    path_parts = tuple(x.replace(".", "_") for x in path_parts)

    return ".".join(path_parts)


def insert_missing_modules(modules: dict[str, types.ModuleType], module_name: str) -> None:
    """
    Used by ``import_path`` to create intermediate modules when using mode=importlib.
    """
    module_parts = module_name.split(".")
    while module_name:
        parent_module_name, _, child_name = module_name.rpartition(".")
        if parent_module_name:
            parent_module = modules.get(parent_module_name)
            if parent_module is None:
                try:
                    if not sys.meta_path:
                        raise ModuleNotFoundError
                    parent_module = importlib.import_module(parent_module_name)
                except ModuleNotFoundError:
                    parent_module = types.ModuleType(
                        module_name,
                        doc="Empty module created by pytest's importmode=importlib.",
                    )
                modules[parent_module_name] = parent_module

            if not hasattr(parent_module, child_name):
                setattr(parent_module, child_name, modules[module_name])

        module_parts.pop(-1)
        module_name = ".".join(module_parts)


def resolve_package_path(path: Path) -> Path | None:
    """
    Return the Python package path by looking for the last directory upwards that still contains an __init__.py.
    """
    result = None
    for parent in itertools.chain((path,), path.parents):
        if parent.is_dir():
            if not (parent / "__init__.py").is_file():
                break
            if not parent.name.isidentifier():
                break
            result = parent
    return result


def resolve_pkg_root_and_module_name(
    path: Path, *, consider_namespace_packages: bool = False
) -> tuple[Path, str]:
    """
    Return the path to the directory of the root package that contains the given Python file, and its module name.
    """
    pkg_root: Path | None = None
    pkg_path = resolve_package_path(path)
    if pkg_path is not None:
        pkg_root = pkg_path.parent
    if consider_namespace_packages:
        start = pkg_root if pkg_root is not None else path.parent
        for candidate in (start, *start.parents):
            module_name = compute_module_name(candidate, path)
            if module_name and is_importable(module_name, path):
                pkg_root = candidate
                break

    if pkg_root is not None:
        module_name = compute_module_name(pkg_root, path)
        if module_name:
            return pkg_root, module_name

    raise CouldNotResolvePathError(f"Could not resolve for {path}")


def is_importable(module_name: str, module_path: Path) -> bool:
    """
    Return if the given module path could be imported normally by Python and matches the specified path.
    """
    try:
        spec = importlib.util.find_spec(module_name)
    except (ImportError, ValueError, ImportWarning):
        return False
    else:
        return spec_matches_module_path(spec, module_path)


def compute_module_name(root: Path, module_path: Path) -> str | None:
    """
    Compute a module name based on a path and a root anchor.
    """
    try:
        path_without_suffix = module_path.with_suffix("")
    except ValueError:
        return None

    try:
        relative = path_without_suffix.relative_to(root)
    except ValueError:
        return None
    names = list(relative.parts)
    if not names:
        return None
    if names[-1] == "__init__":
        names.pop()
    return ".".join(names)


class CouldNotResolvePathError(Exception):
    """Custom exception raised by resolve_pkg_root_and_module_name."""


def scandir(
    path: str | os.PathLike[str],
    sort_key: Callable[[os.DirEntry[str]], object] = lambda entry: entry.name,
) -> list[os.DirEntry[str]]:
    """
    Scan a directory recursively, in breadth-first order.
    The returned entries are sorted according to the given key.
    If the directory does not exist, return an empty list.
    """
    entries = []
    try:
        scandir_iter = os.scandir(path)
    except FileNotFoundError:
        return []
    with scandir_iter as s:
        for entry in s:
            try:
                entry.is_file()
            except OSError as err:
                if _ignore_error(err):
                    continue
                raise
            entries.append(entry)
    entries.sort(key=sort_key)  # type: ignore[arg-type]
    return entries


def visit(
    path: str | os.PathLike[str], recurse: Callable[[os.DirEntry[str]], bool]
) -> Iterator[os.DirEntry[str]]:
    """
    Walk a directory recursively, in breadth-first order.
    Entries at each directory level are sorted.
    """
    entries = scandir(path)
    yield from entries
    for entry in entries:
        if entry.is_dir() and recurse(entry):
            yield from visit(entry.path, recurse)


def absolutepath(path: str | os.PathLike[str]) -> Path:
    """
    Convert a path to an absolute path using os.path.abspath.
    Prefer this over Path.resolve().
    """
    return Path(os.path.abspath(path))


def commonpath(path1: Path, path2: Path) -> Path | None:
    """
    Return the common part shared with the other path, or None if there is no common part.
    """
    try:
        return Path(os.path.commonpath((str(path1), str(path2))))
    except ValueError:
        return None


def bestrelpath(directory: Path, dest: Path) -> str:
    """
    Return a string which is a relative path from directory to dest such that directory/bestrelpath == dest.
    """
    assert isinstance(directory, Path)
    assert isinstance(dest, Path)
    if dest == directory:
        return os.curdir
    base = commonpath(directory, dest)
    if not base:
        return str(dest)
    reldirectory = directory.relative_to(base)
    reldest = dest.relative_to(base)
    return os.path.join(
        *([os.pardir] * len(reldirectory.parts)),
        *reldest.parts,
    )


def safe_exists(p: Path) -> bool:
    """
    Like Path.exists(), but account for input arguments that might be too long.
    """
    try:
        return p.exists()
    except (ValueError, OSError):
        return False
