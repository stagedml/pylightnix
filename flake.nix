{
  description = "Pylightnix flake";

  inputs = {
    # nixpkgs.url = github:grwlf/nixpkgs/local15;
    nixpkgs.url = "path:/home/grwlf/proj/nixcfg/nixpkgs";
  };

  outputs = { self, nixpkgs }:
    let
      defaults = (import ./default.nix) {
        inherit nixpkgs;
        src = self;
      };
    in {
      packages = {
        x86_64-linux = defaults;
      };
      devShells = {
        x86_64-linux = {
          default = defaults.shell;
        };
      };
    };
}
