{ pkgs ?  import <nixpkgs> {}
, stdenv ? pkgs.stdenv
} :
let

  self = pkgs.python36Packages;
  inherit (pkgs) fetchgit;
  inherit (self) buildPythonPackage fetchPypi;

  pyls = self.python-language-server.override { providers=["pycodestyle" "pyflakes"]; };
  pyls-mypy = self.pyls-mypy.override { python-language-server=pyls; };

  env = stdenv.mkDerivation {
    name = "buildenv";
    buildInputs =
    ( with pkgs;
      with self;
    [
      ipython
      pyls-mypy
      pyls
      hypothesis
      pytest
      pytest-mypy
    ]);

    shellHook = with pkgs; ''
      export PYTHONPATH=`pwd`/src:$PYTHONPATH
    '';
  };

in
  env

