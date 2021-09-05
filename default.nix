{ pkgs ?  import <nixpkgs> {}
, python ? pkgs.python37
, doCheck ? true
} :

with python.pkgs;
buildPythonPackage {
  pname = "pylightnix";
  version = "9999";
  src = builtins.filterSource (
    path: type: !( baseNameOf path == "build" && type == "directory" ) &&
                !( baseNameOf path == "dist" && type == "directory" ) &&
                !( baseNameOf path == "result" )
    ) ./.;

  preConfigure = ''
    export PATH="${pkgs.atool}/bin:${pkgs.curl}/bin:${pkgs.wget}/bin:${pkgs.git}/bin:$PATH"
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

  inherit doCheck;
}

