# History

## Next milestones

- 3D Pareto front (w, t, b)
- Standardize cost function
- Sanitize cost function

## X.Y.Z (2026-04-13): Maintenance checkup

### Updates

- **Dependencies**: dropped `pillow` from runtime deps (no direct use; still available transitively via matplotlib). Dropped `rpds-py` from dev deps (unused template leftover). Bumped `ipython>=9.0` for dev setup. matplotlib / dill / numba / zstandard runtime minimums kept at 3.10.8 / 0.4.0 / 0.63.0 / 0.23.0 (prefer newer versions to avoid incompatibilities).
- **Lockfile**: refreshed `uv.lock` (`uv lock --upgrade`) to pull in versions that ship CPython 3.14 wheels on PyPI — notably `numpy 2.4.4`, `numba 0.65`, `contourpy 1.3.3`, `kiwisolver 1.5`, `pyzmq 27`, `zstandard 0.25`, `markupsafe 3.0.3`, `pyyaml 6.0.3`. Also picks up major bumps of dev tooling (`pytest 9`, `sphinx 9`, `myst-parser 5`, `pytest-cov 7`, `ruff 0.15`, `markdown-it-py 4`). This avoids the cold-cache 3.14 CI build rebuilding everything from source (5+ min) after the uv version bump invalidated the previous cache.
- **Tooling**: merged `.coveragerc` into `pyproject.toml` under `[tool.coverage.report]`; added `[tool.ruff]` config (line-length 100, select `E`, `F`, `W`, `I`); removed `--exitfirst --failed-first` from the pytest default `addopts` so CI shows all failures (see `CONTRIBUTING.md` for the local fast-feedback recipe).
- **Pre-commit**: added `.pre-commit-config.yaml` running `pre-commit-hooks` baseline plus `ruff`/`ruff-format`. Contributing guide documents how to install hooks.
- **CI**: bumped `astral-sh/setup-uv` pin from `0.9.30` to `0.11.6` across all three workflows. Migrated the docs workflow away from a `gh-pages` branch to `actions/upload-pages-artifact` + `actions/deploy-pages`; docs now build on pushes to `main` and on PRs only (no more builds on every feature branch). *Action required after release*: flip repo Settings → Pages → Source to "GitHub Actions".
- **Docs**: removed unused `sklearn`/`scipy` intersphinx mappings from `docs/conf.py`.
- **Citation**: updated `citation.cff` abstract to match the generalized (non-fuel-specific) description in `README.md`.
- **`.gitignore`**: added `cov/` to match the coverage HTML output directory.

### Fixes

- `tests/__init__.py`: fixed stale `opti-cruise` docstring leftover from the rebranding.
- `Trajectories.get_traj` / `get_front`: renamed shadowed `t` loop variable to `state` for readability. No behavior change.

## 0.1.1 (2026-02-06): First public release

- Dropped Python 3.10 support (now requires Python 3.11+).
- Fixed type hint in `CostModel` (`down_matrix` was `np.array` instead of `np.ndarray`).
- Removed unused imports in `smart_cruise.py`.
- Updated README with proper quickstart example.
- Fixed documentation issues.

## 0.1.0 (2025-05-15): First release

- First release on PyPI.
