import os
from setuptools import find_packages, setup
from mypyc.build import mypycify

from typed_envs import description, description_addon


setup(
    name="typed-envs",
    url="https://github.com/BobTheBuidler/typed-envs",
    packages=find_packages(),
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
    },
    description=description,
    long_description=description + description_addon,
    author="BobTheBuidler",
    author_email="bobthebuidlerdefi@gmail.com",
    license="MIT",
    setup_requires=["setuptools_scm"],
    package_data={"typed_envs": ["py.typed"]},
    include_package_data=True,
    ext_modules=mypycify(
        paths=[
            "typed_envs/__init__.py",
            "typed_envs/_env_var.py",
            "typed_envs/ENVIRONMENT_VARIABLES.py",
            # TODO: fix mypyc IR error "typed_envs/factory.py",
            "typed_envs/registry.py",
            "typed_envs/typing.py",
            "--pretty",
            "--install-types",
            "--disable-error-code=assignment",
            "--disable-error-code=attr-defined",
        ],
        debug_level=os.environ.get("MYPYC_DEBUG_LEVEL", "0"),
    ),
)
