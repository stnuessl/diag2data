#
# Simple makefile to conveniently run the most important commands
#

PACKAGE_NAME := $(shell \
	python scripts/pyproject-util.py pyproject.toml --key project.name)

PACKAGE_VERSION := $(shell \
	python scripts/pyproject-util.py pyproject.toml --key project.version)

PACKAGE_HOMEPAGE := $(shell \
	python scripts/pyproject-util.py pyproject.toml --key project.urls.homepage)

# Only used for pypi releases in the continuous integration environment.
PACKAGE_SOURCE_LINK := $(PACKAGE_HOMEPAGE)/commit/$(GITHUB_SHA)

BUILD_DIR := build
PACKAGE_TARBALL := $(BUILD_DIR)/$(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz
PACKAGE_WHEEL := $(BUILD_DIR)/$(PACKAGE_NAME)-$(PACKAGE_VERSION)-py3-none-any.whl
PACKAGE_FILES := $(PACKAGE_TARBALL) $(PACKAGE_WHEEL)

VENV_DIR := $(BUILD_DIR)/venv
VENV_PYTHON := $(VENV_DIR)/bin/python

all: package

clean:
	rm -rf $(BUILD_DIR) src/updetect.egg-info

package: $(PACKAGE_FILES)

release: $(PACKAGE_FILES) | $(VENV_PYTHON)
	PACKAGE_NAME=$(PACKAGE_NAME) \
	PACKAGE_VERSION=$(PACKAGE_VERSION) \
	VENV_PYTHON=$(VENV_PYTHON) \
		bash scripts/pypi-release.sh $^

test:
	PYTHONPATH=src python tests/test-diag2data.py

$(PACKAGE_FILES)&:
	@cp README.rst README.bak
	@printf "%s\n" \
			"Release Information" \
			"===================" \
			"" \
			"Based on commit \`$(GITHUB_SHA) <$(PACKAGE_SOURCE_LINK)>\`_." \
			"" >> README.rst
	cat README.rst
	python -m build --outdir $(BUILD_DIR)
	@mv README.bak README.rst

$(VENV_PYTHON):
	python -m venv $(VENV_DIR)


.PHONY: all clean package test release
