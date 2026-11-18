"""Install the source component and its packaged scientific standards."""
from setuptools import setup, find_packages

setup(
    name="Atlas_renew",
    description="Evidence-bound maintenance of existing Atlas complexity brackets",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"oracle_atlas_maintenance": ["resources/*.md", "resources/*.json"]},
    include_package_data=True,
    install_requires=["Atlas_native_backend", "jsonschema"],
    extras_require={
        "responses": ["openai"],
        "codex": ["mcp"],
        "pdf": ["pypdf"],
        "test": ["pytest", "mcp"],
    },
    entry_points={"console_scripts": ["atlas-renew=oracle_atlas_maintenance.cli:main"]},
)
