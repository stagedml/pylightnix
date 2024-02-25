{
  description = "Pylightnix flake";

  inputs = {
    # nixpkgs.url = github:grwlf/nixpkgs/local15;
    nixpkgs.url = "path:/home/grwlf/proj/nixcfg/nixpkgs";
  };

  outputs = { self, nixpkgs }:
    let
      nixpkgsFor = (system: import nixpkgs { inherit system; });

      defaults = system : (import ./default.nix) {
        pkgs = (import nixpkgs){ inherit system ; };
        src = self;
      };
    in {
      packages = {
        x86_64-linux = (defaults "x86_64-linux");
      };
      devShells = {
        x86_64-linux = {
          default = (defaults "x86_64-linux").shell;
        };
      };
    };
}
