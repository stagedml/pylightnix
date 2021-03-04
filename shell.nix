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
    pyyaml
    wheel
  ]);

  nr-types = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.types";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated];
    patchPhase = ''
      sed -i 's/typing//' setup.py
    '';
    src = mypython.pkgs.fetchPypi {
      version = "4.0.2";
      pname = "nr.types";
      sha256 = "sha256:1vslcbx1g07qf7x1izvkg8ns5cj2r4mxq0h3kqy5cpfg85sg6i3c";
    };
  };

  pydoc-markdown = pkgs.python37Packages.buildPythonPackage rec {
    pname = "pydoc-markdown";
    version = "1.0";
    propagatedBuildInputs = with mypython.pkgs ; [nr-types pyyaml];
    doCheck = false; # local HTTP requests don't work
    src = pkgs.fetchFromGitHub {
      owner = "stagedml";
      repo = pname;
      rev = "0662c361b5abca6e1210f94d37c9e244862d9b3a";
      sha256 = "sha256:0vd6bcbjsmw9xpnd9wv7v599d7a6fy0y5wympckip4rqdavzvswv";
    };
  };

  pyls = mypython.pkgs.python-language-server.override { providers=["pycodestyle"]; };
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
      pydoc-markdown

      (let
         mytexlive = texlive.override { python=mypython; };
       in
         mytexlive.combine {
           scheme-medium = mytexlive.scheme-medium;
           inherit (mytexlive) fvextra upquote xstring pgfopts currfile
           collection-langcyrillic makecell ftnxtra minted catchfile framed
           pdflscape environ trimspaces mdframed zref needspace import;
         }
      )
    ]);

    shellHook = with pkgs; ''
      export PYTHONPATH=`pwd`/src:$PYTHONPATH
      export MYPYPATH=`pwd`/src:`pwd`/tests
      # 1980 workaround https://github.com/NixOS/nixpkgs/issues/270#issuecomment-467583872
      export SOURCE_DATE_EPOCH=315532800
    '';
  };
in
  env

