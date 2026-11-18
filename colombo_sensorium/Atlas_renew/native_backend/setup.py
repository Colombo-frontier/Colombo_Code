from pathlib import Path
from setuptools import find_packages, setup

root = Path(__file__).parent
resources = [str(path.relative_to(root / "src/oracle_atlas")) for path in sorted((root / "src/oracle_atlas/resources").rglob("*")) if path.is_file()]
setup(name="Atlas_native_backend", description="Native source and transaction backend for Atlas renewal", packages=find_packages("src"), package_dir={"": "src"}, package_data={"oracle_atlas": resources}, include_package_data=True, python_requires=">=3.11", install_requires=["jsonschema"], extras_require={"openai": ["openai"], "mcp": ["mcp"], "pdf": ["pypdf"]})
