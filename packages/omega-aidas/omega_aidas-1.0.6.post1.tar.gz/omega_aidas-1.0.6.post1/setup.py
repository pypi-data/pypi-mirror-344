from setuptools import setup, find_packages

setup(
    name="omega_aidas",
    version="1.0.6.post1",  # ← Post-release suffix added (no functional change)
    author="Your Name",
    description="OMEGA-AIDAS Python package",
    packages=find_packages(where="generated_code"),
    package_dir={"": "generated_code"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "transformers",
        "tensorflow",
        "torch",
        "pytest",
        "httpx",
    ],
    python_requires=">=3.9",
)