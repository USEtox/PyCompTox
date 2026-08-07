# Releasing

Releases are published **manually with twine**. There is deliberately no
GitHub Actions workflow that uploads to PyPI — see [Why no publish
workflow](#why-no-publish-workflow) below.

## Checklist

1. **Update the version** in `pyproject.toml`.

   `__version__` is read from installed package metadata, so it follows
   `pyproject.toml` automatically and cannot drift.

2. **Update `CHANGELOG.md`** — move entries under a new version heading, and
   spell out any breaking changes with a migration path.

3. **Run the tests.** CI does not run automatically, so this is the only gate:

   ```bash
   pytest                  # full suite, needs COMPTOX_API_KEY
   pytest --run-slow       # optional: also the slow ToxRefDB bulk endpoints
   mypy src/pycomptox --ignore-missing-imports
   flake8 src/ tests/ --select=E9,F63,F7,F82,F401
   mkdocs build --strict
   ```

   If the EPA API is down (503s, dropped connections), the live tests will fail
   for reasons unrelated to the code. `pytest -m "not integration"` still gives
   a meaningful offline signal in that case.

4. **Build and check the artifacts:**

   ```bash
   rm -rf dist build src/*.egg-info
   uv build
   twine check dist/*
   ```

   `uv build` is used rather than `python -m build` because the latter needs
   `python3.N-venv` installed for build isolation, which is easy to be missing.

5. **Verify the wheel** before uploading — these are the things that have
   actually gone wrong before:

   ```bash
   python -c "
   import zipfile
   z = zipfile.ZipFile('dist/comptox_python-X.Y.Z-py3-none-any.whl')
   n = z.namelist()
   for w in ['pycomptox/__init__.py', 'pycomptox/py.typed']:
       assert w in n, f'MISSING {w}'
   assert not [x for x in n if x.startswith('tests/')], 'tests leaked into wheel'
   print('ok')
   "
   ```

   A missing `__init__.py` is what broke 0.6.0's entire public API.

6. **Tag and push:**

   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin vX.Y.Z
   ```

7. **Upload:**

   ```bash
   twine upload dist/*
   ```

   Credentials come from `~/.pypirc` (`[pypi]` with `username = __token__`).

8. **Verify the published release** installs cleanly from PyPI:

   ```bash
   uv venv /tmp/relcheck && \
   uv pip install --python /tmp/relcheck/bin/python --no-cache "comptox-python==X.Y.Z" && \
   COMPTOX_API_KEY=dummy /tmp/relcheck/bin/python -c "
   import pycomptox
   assert pycomptox.__file__ is not None      # not a namespace package
   print(pycomptox.__version__)
   from pycomptox import Chemical, save_api_key
   print('ok')
   "
   ```

## Uploads are irreversible

A PyPI version can be *yanked* but never deleted or reused. Get steps 3–5 right
before step 7; there is no undo.

## Why no publish workflow

`.github/workflows/publish.yml` used to publish on `release: published` via
PyPI Trusted Publishing. It was removed so that twine is the single publishing
path, which means:

- **Do not create a GitHub Release expecting it to publish.** Nothing listens
  for that event any more.
- If you want automated publishing back, note that the PyPI-side Trusted
  Publisher entry may still exist for this repository. Check it at
  <https://pypi.org/manage/project/comptox-python/settings/publishing/> before
  re-adding any workflow, and remove that entry if automated publishing is not
  wanted.
