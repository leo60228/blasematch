{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { nixpkgs, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlay (self: super: {
            qhull = super.qhull.overrideAttrs (old: {
              src = super.fetchFromGitHub {
                owner = "qhull";
                repo = "qhull";
                rev = "d0e8064088e0d51f7df9b380b22d66a3c6ba0c9a";
                sha256 = "0g009w5mzidxgvj6p90gd7rrhp325cslmgfd5b64vrxqjswcpydk";
              };
            });
          }) ];
        };
        poetryEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          overrides = pkgs.poetry2nix.defaultPoetryOverrides.overrideOverlay (self: super: {
            pyarrow = super.pyarrow.override {
              preferWheel = true;
            };
            matplotlib = super.matplotlib.overrideAttrs (old: {
              propagatedBuildInputs = (old.propagatedBuildInputs or [ ]) ++ [ self.certifi pkgs.qhull pkgs.freetype ];
              postPatch = ''
              cat > setup.cfg << EOF
              [libs]
              system_freetype = True
              system_qhull = True
              EOF
              '';
            });
            aiohttp-sse-client = super.aiohttp-sse-client.overridePythonAttrs (
              old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ self.pytest-runner ];
              }
            );
          });
        };
      in {
        devShell = pkgs.mkShell {
          nativeBuildInputs = [ poetryEnv pkgs.python38Packages.poetry ];
        };
      }
    );
}
