{ pkgs ?  import <nixpkgs> {}
, python ? pkgs.python36
, doCheck ? false
} :

with python.pkgs;
buildPythonPackage {
  pname = "pylightnix";
  version = "0.0.2";
  src = builtins.filterSource (
    path: type: !( baseNameOf path == "build" && type == "directory" ) &&
                !( baseNameOf path == "result" ) ) ./.;

  preConfigure = ''
    export PATH=${pkgs.wget}/bin:${pkgs.atool}/bin:$PATH
  '';

  checkInputs = [ pytest pytest-mypy hypothesis ];

  checkPhase = ''
    pytest
  '';

  inherit doCheck;
}

