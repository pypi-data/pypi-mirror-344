# Changelog

All notable changes to the project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.2] - 2025-04-28

- Transitioned from `poetry` to `uv` for packaging and test environment generation.
- Make some Python/NumPy version compatibility improvments (static and runtime). MyPy
  testing requires setting `--always-true NUMPY_1_23` if NumPy >= 1.23.0 (otherwise set
  `--always-false`).
- Added more version tests.

## [2.0.1] - 2024-05-16

Make exports in `__init__.py` explicit.

## [2.0.0.post0] - 2024-05-16

Readme updates, format markdown 90 char.

## [2.0.0] - 2024-05-15

- **BREAKING CHANGE** - Drop support for supplying dtype as a string
- **BREAKING CHANGE** - `lock` removed from `SharedNDArray`. It didn't make sense to have
  it on there since SharedNDArray should be serializable and `multiprocessing.Lock` is
  not.
- `from_array()` and `from_shape` individual functions added to the  `shared_ndarray`
  module. They are indentical to the classmethods in `SharedNDArray` but properly
  specialize the type when using Pyright. MyPy is happy either way.
- Add a couple tests
- Change to ruff, max line length 90

## [1.1.0] - 2021-01-13

- Type input for creating a `SharedNDArray` can now be a NumPy scalar type, constrained to
  only those types with a fixed number of bytes per element. SharedNDArray can get its
  static type from the dtype.
- Add overloads to `__init__()` and `__getitem__()`.
- Use `single-version` to track version number from `pyproject.toml`.

## [1.0.3] - 2023-01-12

- Added py.typed
- Minor refactors/typing fixes

## [1.0.2] - 2022-02-09

- Fixed missing import

## [1.0.1] - 2022-02-09

- Some typing fixes

## [1.0.0] - 2021-08-11

- Initial release

[Unreleased]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v2.0.2...master
[2.0.2]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v2.0.1...v2.0.2
[2.0.1]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v2.0.0.post0...v2.0.1
[2.0.0.post0]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v2.0.0...v2.0.0.post0
[2.0.0]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v1.1.0...v2.0.0
[1.1.0]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v1.0.3...v1.1.0
[1.0.3]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v1.0.2...v1.0.3
[1.0.2]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v1.0.1...v1.0.2
[1.0.1]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/compare/v1.0.0...v1.0.1
[1.0.0]: https://gitlab.com/osu-nrsg/shared-ndarray2/-/tags/v1.0.0
