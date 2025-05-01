from configparser import ConfigParser
from pathlib import Path
from uuid import uuid4
from PySide6.QtCore import QProcessEnvironment


class MyConfig:
    def __init__(self, dev_mode: bool):
        config_dir = self._get_config_file(dev_mode)
        self.LOGFILE_PATH = config_dir / 'phystool.log'

        conf = ConfigParser()
        conf.read(self._config_file)
        self._dbs = {
            name: Path(path).expanduser()
            for name, path in conf.items('db')
        }

        self.AUX_DIR = _ensure_exists(config_dir / "texaux")
        self.DELTA_THEME = conf['git']['theme']
        self.EDITOR_CMD: tuple[str, list[str]] = (conf['physnoob']['editor'], [])
        if self.EDITOR_CMD[0] == "vim":
            self.EDITOR_CMD = ("rxvt-unicode", ["-e", "vim"])

        self.load_db_conf(next(iter(self._dbs)))  # get first db name

    def __str__(self) -> None:
        return (
            f"{self.DB_DIR       = !s}\n"  # noqa
            f"{self.LATEX.source = !s}\n"  # noqa
            f"{self.AUX_DIR      = !s}\n"  # noqa
            f"{self.EDITOR_CMD   = !s}\n"  # noqa
            f"{self.DELTA_THEME  = !s}\n"  # noqa
        )

    def _get_config_file(self, dev_mode: bool) -> Path:
        config_dir = (
            Path(__file__).parents[2] / "dev"
            if dev_mode
            else Path.home() / ".phystool"
        )

        self._config_file = config_dir / "phystool.conf"
        if not self._config_file.exists():
            raise ValueError
            from shutil import (
                copyfile,
                copytree,
                ignore_patterns
            )
            static = self.get_static_path()
            copyfile(
                static / "phystool.conf",
                self._config_file
            )
            copytree(
                (
                    config_dir / "physdb_dev"
                    if dev_mode
                    else static / "physdb_dev"
                ),
                Path.home() / "physdb",
                ignore=ignore_patterns(".git*")
            )  # FIXME: exclude those files within pyproject.yaml
        return config_dir

    def load_db_conf(self, name: str) -> None:
        self.DB_DIR = self._dbs[name]
        if not self.DB_DIR.exists():
            raise FileNotFoundError(
                f"Database not found, looking for '{self.DB_DIR}'"
            )

        self.LATEX = LaTeXConf(db_dir=self.DB_DIR)
        self.METADATA_DIR = _ensure_exists(self.DB_DIR / "metadata")
        self.METADATA_PATH = self.METADATA_DIR / '0_metadata.pkl'
        self.TAGS_PATH = self.METADATA_DIR / '1_tags.json'
        self.EVALUATION_PATH = self.METADATA_DIR / '2_evaluations.json'

    def get_static_path(self) -> Path:
        return Path(__file__).parent / "static"

    def new_pdb_filename(self) -> Path:
        return (self.DB_DIR / str(uuid4())).with_suffix(".tex")

    def save_config(self, section: str, key: str, val: str) -> None:
        conf = ConfigParser()
        conf.read(self._config_file)
        try:
            conf[section][key] = val
        except KeyError:
            conf.add_section(section)
            conf[section][key] = val
        with self._config_file.open('w') as out:
            conf.write(out)


class LaTeXConf:
    def __init__(self, db_dir: Path):
        self.source = _ensure_exists(db_dir / "phystex")

        conf = ConfigParser()
        conf.read(self.source / "latex.conf")

        self.access = conf['db']['access']
        self.tikz_pattern = fr"^\\documentclass.*{{{conf['latex']['tikz']}}}"
        self._template = (
            f"\\documentclass{{{{{conf['latex']['auto']}}}}}\n"
            f"\\PdbSetDBPath{{{{{db_dir}/}}}}\n"
            "\\begin{{document}}\n"
            "    \\PdbPrint{{{tex_file}}}\n"
            "\\end{{document}}"
        )
        self._env: dict[bool, QProcessEnvironment | dict] = {}

    def env(self, qrocess: bool) -> dict[str, str] | QProcessEnvironment:
        if not self._env:
            tmp = QProcessEnvironment.systemEnvironment()
            tmp.insert("TEXINPUTS", f":{self.source}:")
            self._env = {
                True: tmp,
                False: {
                    key: tmp.value(key)
                    for key in tmp.keys()
                }
            }
        return self._env[qrocess]

    def template(self, tex_file: Path) -> str:
        return self._template.format(tex_file=tex_file)


def _ensure_exists(path: Path) -> Path:
    if not path.exists():
        path.mkdir()
    return path
