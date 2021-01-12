{ pkgs ?  import <nixpkgs> {}
, python ? pkgs.python36
, doCheck ? true
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
    export PATH="${pkgs.atool}/bin:${pkgs.wget}/bin:${pkgs.git}/bin:$PATH"
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
    export PATH="${pkgs.atool}/bin:${pkgs.wget}/bin:$PATH"
    pytest
  '';

  inherit doCheck;
}

