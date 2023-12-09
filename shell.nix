{ pkgs ?  import <nixpkgs> {}
, stdenv ? pkgs.stdenv
} :
let
  python3 = pkgs.python3;

  local = rec {

    python-dev = python3.withPackages (
      pp: let
        pylsp = pp.python-lsp-server;
        pylsp-mypy = pp.pylsp-mypy.override { python-lsp-server=pylsp; };
      in with pp; [
      setuptools
      setuptools_scm
      ipython
      hypothesis
      pytest
      pytest-mypy
      pytest_xdist
      # Pweave
      coverage
      pylsp
      pylsp-mypy
      pyyaml
      wheel
      scipy
      matplotlib
      pyqt5
      twine

      pydoc-markdown
      codecov
    ]);

    env = pkgs.mkShell {
      name = "shell";
      buildInputs = with pkgs; with self; [
        gnumake
        cloc
        python-dev

        (let
           mytexlive = texlive.override { python3=python-dev; };
         in
           mytexlive.combine {
             scheme-medium = mytexlive.scheme-medium;
             inherit (mytexlive) fvextra upquote xstring pgfopts currfile
             collection-langcyrillic makecell ftnxtra minted catchfile framed
             pdflscape environ trimspaces mdframed zref needspace import;
           }
        )
      ];

      shellHook = with pkgs; ''
        export PYTHONPATH=`pwd`/src:$PYTHONPATH
        export MYPYPATH=`pwd`/src:`pwd`/tests
        export QT_QPA_PLATFORM_PLUGIN_PATH=`echo ${pkgs.qt5.qtbase.bin}/lib/qt-*/plugins/platforms/`
        # 1980 workaround https://github.com/NixOS/nixpkgs/issues/270#issuecomment-467583872
        export SOURCE_DATE_EPOCH=315532800
        alias ipython="sh $(pwd)/ipython.sh"
      '';
    };

    collection = {
      inherit env;
    };
  };

in
  local.collection

