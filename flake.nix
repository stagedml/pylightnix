{
  description = "Pylightnix flake";

  inputs = {
    # nixpkgs.url = github:grwlf/nixpkgs/local12;
    nixpkgs.url = "path:/home/grwlf/proj/nixcfg/nixpkgs";
  };

  outputs = { self, nixpkgs }: {

    defaultPackage.x86_64-linux =
      with import nixpkgs { system = "x86_64-linux"; };
      let
        python = python3;
        doCheck = true;
        version = "0.3";
      in
      with python.pkgs;
      buildPythonPackage {
        pname = "pylightnix";
        inherit version;
        src = builtins.filterSource (
          path: type: !( baseNameOf path == "build" && type == "directory" ) &&
                      !( baseNameOf path == "dist" && type == "directory" ) &&
                      !( baseNameOf path == "result" )
          ) ./.;

        preConfigure = ''
          export PATH="${atool}/bin:${curl}/bin:${wget}/bin:${git}/bin:$PATH"
        '';

        buildInputs = [ setuptools_scm ];

        checkInputs = [ pytest pytest-mypy hypothesis pytest_xdist];

        SETUPTOOLS_SCM_PRETEND_VERSION = version;

        checkPhase = ''
          export PATH=\
          "${atool}/bin:${curl}/bin:${wget}/bin:"\
          "${zip}/bin:${unzip}/bin:$PATH"
          pytest -n `nproc`
        '';

        inherit doCheck;
      };
  };
}
