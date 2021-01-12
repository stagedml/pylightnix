{ pkgs ?  import <nixpkgs> {}
, stdenv ? pkgs.stdenv
} :
let
  mypython = pkgs.python37.withPackages (
    pp: with pp; [
      ipython
      hypothesis
      pytest
      pytest-mypy
      Pweave
      coverage
      python-language-server
    ]);

  pyls = mypython.pkgs.python-language-server.override { providers=["pycodestyle" "pyflakes"]; };
  pyls-mypy = mypython.pkgs.pyls-mypy.override { python-language-server=pyls; };

  env = stdenv.mkDerivation {
    name = "buildenv";
    buildInputs =
    ( with pkgs;
      with self;
    [
      gnumake
      mypython
      pyls
      pyls-mypy
    ]);

    shellHook = with pkgs; ''
      export PYTHONPATH=`pwd`/src:$PYTHONPATH
    '';
  };
in
  env

