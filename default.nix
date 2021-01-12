{ pkgs ?  import <nixpkgs> {}
, python ? pkgs.python36
, doCheck ? false
} :

with python.pkgs;
buildPythonPackage {
  pname = "pylightnix";
  version = "0.2.0";
  src = builtins.filterSource (
    path: type: !( baseNameOf path == "build" && type == "directory" ) &&
                !( baseNameOf path == "result" )
    ) ./.;

  preConfigure = ''
    export PYLIGHTNIX_AUNPACK="${pkgs.atool}/bin/aunpack"
    export PYLIGHTNIX_WGET="${pkgs.wget}/bin/wget"
    export PATH="${pkgs.git}/bin:$PATH"
    if ! test -d /build/pylightnix/.git ; then
      echo "Looks like Pylightnix is a submodule of some other repo."\
           "\`nix-build\` is unable to detect its version, unfortunately."\
           "Please checkout Pylightnix as a normal Git repository"\
           "and retry." >&2
      exit 1
    fi
  '';

  buildInputs = [ pytest pytest-mypy hypothesis setuptools_scm ];

  inherit doCheck;
}

