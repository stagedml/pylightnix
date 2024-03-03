{
  description = "Pylightnix flake";

  nixConfig = {
    bash-prompt = "[ \\w Pylightnix-DEV] $ ";
  };

  inputs = {
    # nixpkgs.url = github:grwlf/nixpkgs/local15;
    nixpkgs = {
      url = "path:/home/grwlf/proj/nixcfg/nixpkgs";
    };

    litrepl = {
      url = "github:grwlf/litrepl.vim";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, litrepl }:
    let
      nixpkgsFor = (system: import nixpkgs { inherit system; });

      defaults = system : (import ./default.nix) {
        pkgs = (import nixpkgs){ inherit system ; };
        litrepl = litrepl.outputs.packages.${system};
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
