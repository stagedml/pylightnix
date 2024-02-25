{ pkgs ?  import <nixpkgs> {}
, src ? builtins.filterSource (
        path: type: !( baseNameOf path == "build" && type == "directory" ) &&
                    !( baseNameOf path == "dist" && type == "directory" ) &&
                    !( baseNameOf path == "result" )
        ) ./.
} :

let

  python = pkgs.python3;

  local = rec {

    inherit (pkgs) atool curl wget git;

    python-dev = pkgs.python3.withPackages (
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
      pytest-cov
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

      # (pydoc-markdown pp)
      codecov
    ]);


    pylightnix = with python.pkgs; buildPythonPackage {
      pname = "pylightnix";
      version = "9999";
      inherit src;

      preConfigure = ''
        export PATH="${atool}/bin:${curl}/bin:${wget}/bin:${git}/bin:$PATH"
        if ! test -d /build/pylightnix/.git ; then
          echo "Looks like Pylightnix is a submodule of some other repo."\
               "\`nix-build\` is unable to detect its version, unfortunately."\
               "Please checkout Pylightnix as a normal Git repository"\
               "and retry." >&2
          exit 1
        fi
      '';

      buildInputs = [ setuptools_scm ];

      checkInputs = [ pytest pytest-mypy hypothesis ];

      checkPhase = ''
        export PATH=\
        "${pkgs.atool}/bin:${pkgs.curl}/bin:${pkgs.wget}/bin:"\
        "${pkgs.zip}/bin:${pkgs.unzip}/bin:$PATH"
        pytest
      '';

      doCheck = true;
    };

    shell = pkgs.mkShell {
      name = "shell";
      buildInputs = with pkgs; [
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
        export QT_QPA_PLATFORM_PLUGIN_PATH=`echo ${qt5.qtbase.bin}/lib/qt-*/plugins/platforms/`
        # 1980 workaround https://github.com/NixOS/nixpkgs/issues/270#issuecomment-467583872
        export SOURCE_DATE_EPOCH=315532800
        alias ipython="sh $(pwd)/ipython.sh"
      '';
    };

    collection = {
      inherit pylightnix shell;
    };

  };
in
  local.collection
