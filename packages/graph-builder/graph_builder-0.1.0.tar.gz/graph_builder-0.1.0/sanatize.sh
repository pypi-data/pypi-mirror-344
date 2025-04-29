#!/bin/bash

pre-commit run --all-files

black graph_builder

ruff check graph_builder
ruff format graph_builder
