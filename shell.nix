{ pkgs ?  import <nixpkgs> {}
, stdenv ? pkgs.stdenv
} :
let

  mypython = pkgs.python37.withPackages (
    pp: let
      pyls = pp.python-language-server.override { providers=["pycodestyle"]; };
      pyls-mypy = pp.pyls-mypy.override { python-language-server=pyls; };
    in with pp; [
    ipython
    hypothesis
    pytest
    pytest-mypy
    Pweave
    coverage
    pyls
    pyls-mypy
    pyyaml
    wheel
    scipy
    pyqt5
  ]);

  codecov = pkgs.python37Packages.buildPythonPackage rec {
    pname = "codecov";
    version = "2.1.10";

    src = pkgs.python37Packages.fetchPypi {
      inherit pname version;
      sha256 = "d30ad6084501224b1ba699cbf018a340bb9553eb2701301c14133995fdd84f33";
    };
    checkInputs = with pkgs.python37Packages; [ unittest2 ]; # Tests only
    propagatedBuildInputs = with pkgs.python37Packages; [ requests coverage ];
    postPatch = ''
      sed -i 's/, "argparse"//' setup.py
    '';
    # No tests in archive
    doCheck = false;
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

  # {{{ Newer pydoc-markdown, doesn't work due to te.TypeGuard error
  nr-pylang-utils = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.pylang.utils";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated];
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    doCheck = false;
    src = mypython.pkgs.fetchPypi {
      version = "0.1.3";
      pname = "nr.pylang.utils";
      sha256 = "sha256:0dwqhrw692z35dhvqyhc2dkh4kli86im4j6fiz6fy2wa53kfljx5";
    };
  };

  nr-stream = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.stream";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated nr-pylang-utils];
    doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    src = mypython.pkgs.fetchPypi {
      version = "0.2.3";
      pname = "nr.stream";
      sha256 = "sha256:14k5vd23cnmm5j3c0a1z82a803w5x0sisxadzhj2vch0q663rjbn";
    };
  };

  nr-utils-re = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.utils.re";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated ];
    doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    src = mypython.pkgs.fetchPypi {
      version = "0.3.1";
      pname = name;
      sha256 = "sha256:148hc5adwnmpbm2fh2x16fw4fll2bpw6j2qz6vspxy106qqkjiby";
    };
  };

  nr-parsing-date = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.parsing.date";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated nr-utils-re
    deprecated ];
    doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    patchPhase = ''
      sed -i "s/'dataclasses .*//" setup.py
      '';
    src = mypython.pkgs.fetchPypi {
      version = "1.0.3";
      pname = name;
      sha256 = "sha256:1mxkyr57kfqavh2kf6g58cpk0br6kq261islwk9ahii87jazxm6v";
    };
  };

  nr-preconditions = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.preconditions";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated ];
    doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    # patchPhase = ''
    #   sed -i "s/'dataclasses .*//" setup.py
    #   '';
    src = mypython.pkgs.fetchPypi {
      version = "0.0.4";
      pname = name;
      sha256 = "sha256:0kgsyfk0wyqksyz8rwsdg3szii8pvih6rhl0fwv4pwq0jndizfc6";
    };
  };

  nr-optional = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.optional";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated ];
    doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    # patchPhase = ''
    #   sed -i "s/'dataclasses .*//" setup.py
    #   '';
    src = mypython.pkgs.fetchPypi {
      version = "0.2.0";
      pname = name;
      sha256 = "sha256:022cvyiglgm1d5ay6g7p0zjl6nsxw7pnnzv449bn5283ymriz00v";
    };
  };

  nr-fs = pkgs.python37Packages.buildPythonPackage rec {
    name = "nr.fs";
    propagatedBuildInputs = with mypython.pkgs ; [six deprecated ];
    doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    # patchPhase = ''
    #   sed -i "s/'dataclasses .*//" setup.py
    #   '';
    src = mypython.pkgs.fetchPypi {
      version = "1.6.3";
      pname = name;
      sha256 = "sha256:0jhjvzy5mdgvh1vx6fskpqrfjwh81k68rg25a9fgjhs19jha12kq";
    };
  };

  te = mypython.pkgs.typing-extensions.overridePythonAttrs rec {
    version = "3.10.0.0";
    src = mypython.pkgs.fetchPypi {
      pname = "typing_extensions";
      version = version;
      sha256 = "0hpkrp39w58f6lc6r0jhn97qhcp95z49vyan0ryj2x4ihibz3djh";
    };
  };

  databind-core = pkgs.python37Packages.buildPythonPackage rec {
    name = "databind.core";
    propagatedBuildInputs = with mypython.pkgs ; [
      nr-parsing-date nr-stream nr-preconditions nr-optional te ];
    # docheck = false;
    # patchphase = ''
    # '';
    doCheck = false;
    patchPhase = ''
      # sed -i "s/'typing_extensions.*//" setup.py
      # sed -i 's/typing_extensions >=3.10.0/typing_extensions >=3.7.0/' setup.py
      sed -i 's/Deprecated >=1.2.12/Deprecated >=1.2.7/' setup.py
    '';
    src = mypython.pkgs.fetchPypi {
      version = "1.2.0";
      pname = name;
      sha256 = "sha256:0lvpbmsplj8fpnhvp2si4g1afjjv1r6p6gfbmlga02kza0wx4rgh";
    };
  };

  databind-json = pkgs.python37Packages.buildPythonPackage rec {
    name = "databind.json";
    propagatedBuildInputs = with mypython.pkgs ; [ te databind-core ];
    # docheck = false;
    # patchphase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    patchPhase = ''
      # sed -i "s/'typing_extensions.*//" setup.py
      # sed -i 's/typing_extensions >=3.10.0/typing_extensions >=3.7.0/' setup.py
      sed -i 's/Deprecated >=1.2.12/Deprecated >=1.2.7/' setup.py
    '';
    src = mypython.pkgs.fetchPypi {
      version = "1.2.0";
      pname = name;
      sha256 = "sha256:0nra3wgm9nnfzr3wq94dvh3yj38yyd5c6fka7lbw5yikj0x2y7ri";
    };
  };

  docspec-python = pkgs.python37Packages.buildPythonPackage rec {
    name = "docspec-python";
    propagatedBuildInputs = with mypython.pkgs ; [ te databind-core databind-json
    docspec ];
    # doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    src = mypython.pkgs.fetchPypi {
      version = "1.0.1";
      pname = name;
      sha256 = "sha256:11in75xpv301w99il00g8a854hbfywi0w1485z7b87byb2yj1b03";
    };
  };


  docspec = pkgs.python37Packages.buildPythonPackage rec {
    name = "docspec";
    propagatedBuildInputs = with mypython.pkgs ; [ te databind-core databind-json ];
    # doCheck = false;
    # patchPhase = ''
    #   sed -i 's/typing//' setup.py
    # '';
    src = mypython.pkgs.fetchPypi {
      version = "1.0.1";
      pname = name;
      sha256 = "sha256:18pxhrp2xmg0a4qwrfhi5lnij453zkjjcbdkzmkcpjygs1r1rl71";
    };
  };

  pydoc-markdown2 = pkgs.python37Packages.buildPythonPackage rec {
    pname = "pydoc-markdown";
    version = "4.2.0";
    propagatedBuildInputs = with mypython.pkgs ; [
      te pyyaml nr-stream nr-pylang-utils requests pyyaml watchdog
      docspec docspec-python click nr-fs toml ];
    patchPhase = ''
      sed -i 's/requests >=2.23.0/requests >=2.22.0/' setup.py
      sed -i 's/PyYAML >=5.3.0/PyYAML >=5.2.0/' setup.py
      sed -i 's/toml >=0.10.1/toml >=0.10.0/' setup.py
    '';
    doCheck = false; # local HTTP requests don't work
    src = pkgs.fetchFromGitHub {
      owner = "NiklasRosenstein";
      repo = pname;
      rev = "c3b9713ec11965ad1c978ba846323a0d998ec85a";
      sha256 = "sha256:0zlxrabbx00ky7c5vwbqm3376w4lnna8dbsl3gdsrmd5aynyhkcj";
    };
  };
  # }}}

  env = stdenv.mkDerivation {
    name = "buildenv";
    buildInputs =
    ( with pkgs;
      with self;
    [
      gnumake
      mypython
      pydoc-markdown
      codecov

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
      export QT_QPA_PLATFORM_PLUGIN_PATH=`echo ${pkgs.qt5.qtbase.bin}/lib/qt-*/plugins/platforms/`
      # 1980 workaround https://github.com/NixOS/nixpkgs/issues/270#issuecomment-467583872
      export SOURCE_DATE_EPOCH=315532800
      alias ipython="sh $(pwd)/ipython.sh"
    '';
  };
in
  env

