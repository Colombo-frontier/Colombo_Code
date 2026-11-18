"""Copy the same project resources during builds; do not manually maintain a second set of runtime prompts."""
from pathlib import Path
from shutil import copytree, copy2
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class BuildWithResources(build_py):
    def run(self):
        super().run()
        root=Path(__file__).parent
        target=Path(self.build_lib)/"oracle_atlas"/"resources"
        target.mkdir(parents=True,exist_ok=True)
        for folder in ["agents","skills","standards","schemas","config"]:
            copytree(root/folder,target/folder,dirs_exist_ok=True)
        for name in ["protocol.md","AGENTS.md"]:copy2(root/name,target/name)


setup(
    name="structural-exploration",
    description="Structural exploration of oracle settings with independent research, review, and Atlas publication",
    long_description=(Path(__file__).parent / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    python_requires=">=3.11",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"oracle_atlas": ["resources/**/*", "resources/*"]},
    include_package_data=True,
    install_requires=["jsonschema>=4.18,<5"],
    extras_require={
        "openai": ["openai>=1.99,<3"],
        "mcp": ["mcp>=1.12,<2"],
        "pdf": ["pypdf>=5,<7"],
        "all": ["openai>=1.99,<3", "mcp>=1.12,<2", "pypdf>=5,<7"],
        "test": ["pytest>=8,<10"],
    },
    entry_points={"console_scripts": [
        "structural-exploration=oracle_atlas.expansion.cli:structural_main",
        "oracle-atlas=oracle_atlas.cli:main",
        "oracle-atlas-expand=oracle_atlas.expansion.cli:main",
    ]},
    cmdclass={"build_py": BuildWithResources},
)

