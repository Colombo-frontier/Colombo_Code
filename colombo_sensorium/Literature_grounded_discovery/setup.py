"""Copy the same project resources during builds; do not manually maintain a second set of runtime prompts."""
from pathlib import Path
from shutil import copytree, copy2, ignore_patterns
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class BuildWithResources(build_py):
    def run(self):
        super().run()
        root=Path(__file__).parent
        target=Path(self.build_lib)/"oracle_atlas"/"resources"
        target.mkdir(parents=True,exist_ok=True)
        for folder in ["agents","skills","standards","schemas","config"]:
            copytree(root/folder,target/folder,dirs_exist_ok=True,ignore=ignore_patterns(".DS_Store", "__pycache__", "*.pyc"))
        for name in ["protocol.md","AGENTS.md"]:copy2(root/name,target/name)


setup(
    name="Literature_grounded_discovery",
    description="Literature discovery, independent review, and transactional Atlas maintenance",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"oracle_atlas": ["resources/**/*", "resources/*"]},
    include_package_data=True,
    install_requires=["jsonschema"],
    extras_require={
        "openai": ["openai"],
        "mcp": ["mcp"],
        "pdf": ["pypdf"],
        "all": ["openai", "mcp", "pypdf"],
        "test": ["pytest"],
    },
    entry_points={"console_scripts": ["oracle-atlas=oracle_atlas.cli:main"]},
    cmdclass={"build_py": BuildWithResources},
)
