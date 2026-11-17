import re

from backend.migrate import MIGRATIONS_DIR

NAME = re.compile(r"^(\d{3})_[a-z0-9_]+\.sql$")


def _files():
    return sorted(MIGRATIONS_DIR.glob("*.sql"))


def test_migration_files_exist():
    assert _files(), "no migration files found"


def test_migration_names_are_numbered():
    for path in _files():
        assert NAME.match(path.name), f"bad migration name: {path.name}"


def test_migration_numbers_have_no_gaps_or_repeats():
    numbers = [int(NAME.match(p.name).group(1)) for p in _files()]
    assert numbers == list(range(1, len(numbers) + 1))


def test_migration_files_are_not_empty():
    for path in _files():
        assert path.read_text(encoding="utf-8").strip(), path.name
