# -*- coding: utf-8 -*-
# :Project:   PatchDB — Development environment
# :Created:   dom 26 giu 2022, 11:48:09
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023, 2024, 2025 Lele Gaifax
#

{
  description = "metapensiero.sphinx.patchdb";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) fromTOML readFile;
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) flip;
        inherit (gitignore.lib) gitignoreFilterWith;

        pinfo = (fromTOML (readFile ./pyproject.toml)).project;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        # List of supported Python versions, see also Makefile
        snakes = flip map [ "311" "312" "313" ]
          (ver: rec { name = "python${ver}"; value = builtins.getAttr name pkgs;});

        mkBMVPkg = python:
          let
            httpx' = python.pkgs.httpx.overridePythonAttrs rec {
              version = "0.28.1";
              src = python.pkgs.fetchPypi {
                inherit version;
                pname = "httpx";
                hash = "sha256-demMXxaw81tWeFb1l/Bv8icKN0RwpcI5IkJSjj4+Qvw=";
              };
            };
          in
            python.pkgs.buildPythonPackage rec {
              pname = "bump-my-version";
              version = "1.1.2";
              src = python.pkgs.fetchPypi {
                pname = "bump_my_version";
                inherit version;
                hash = "sha256-ASKEWnhQK1paY1yhfB77Ph7AXnfXLROyMUGGuYBogvs=";
              };
              pyproject = true;
              build-system = [ python.pkgs.hatchling ];
              dependencies = with python.pkgs; [
                click
                httpx'
                pydantic
                pydantic-settings
                questionary
                rich
                rich-click
                tomlkit
                wcmatch
              ];
            };

        mkPatchDBPkg = python: python.pkgs.buildPythonPackage {
          pname = pinfo.name;
          version = pinfo.version;

          src = getSource "patchdb" ./.;
          pyproject = true;

          dependencies = (with python.pkgs; [
            enlighten
            # As of Sat Apr 20 09:29:59 2024 nixpkgs still has 0.4.4
            (sqlparse.overridePythonAttrs rec {
              pname = "sqlparse";
              version = "0.5.1";
              src = pkgs.fetchPypi {
                inherit pname version;
                hash = "sha256-u2tN9GVlXvMyVI4k8I4gWvyBuauGyxxFZXp/8XOjoA4=";
              };
              pyproject = true;
              format = null;
              build-system = [ hatchling ];
            })
          ]);

          build-system = (with python.pkgs; [
            pdm-backend
          ]);

          doCheck = false;
        };

        patchDBPkgs = flip map snakes
          (py: {
            name = "patchdb-${py.name}";
            value = mkPatchDBPkg py.value;
          });

        mkTestShell = python:
          let
            patchdb = mkPatchDBPkg python;
            bump-my-version = mkBMVPkg python;
            pyenv = python.buildEnv.override {
              extraLibs = (with python.pkgs; [
                bump-my-version
                patchdb
                psycopg
                docutils
                pytest
                sphinx
              ]);
            };
          in
            pkgs.mkShell {
              name = "Test Python ${python.version}";
              packages = [
                pyenv
              ] ++ (with pkgs; [
                gnumake
                just
                postgresql_16
              ]);

              shellHook = ''
                export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
              '';

              LANG="C";
            };

        testShells = flip map snakes
          (py: {
            name = "test-${py.name}";
            value = mkTestShell py.value;
          });
      in {
        devShells =
          let
            bump-my-version = mkBMVPkg pkgs.python3;
            pydevenv = pkgs.python3.buildEnv.override {
              extraLibs = (with pkgs.python3Packages; [
                bump-my-version
                babel
                build
                twine
              ]);
            };
          in {
            default = pkgs.mkShell {
              name = "Dev shell";

              packages = with pkgs; [
                gnumake
                just
                pydevenv
              ];

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        } // builtins.listToAttrs testShells;

        lib = {
          inherit mkPatchDBPkg;
        };

        packages = (builtins.listToAttrs patchDBPkgs);
      });
}
