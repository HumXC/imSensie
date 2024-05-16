{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, flake-utils, nixpkgs }:
    flake-utils.lib.eachSystem [ "x86_64-linux" ] (system:
      let
        pkgs = import nixpkgs { inherit system; };
        py = (pkgs.python311.withPackages (ps: with ps; [
          pip
        ]));
      in
      {
        devShells.default = with pkgs; mkShell {
          packages = [
            py
          ];
          NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
            libGL
            zlib
            glib
            stdenv.cc.cc
            xorg.libxcb
            xorg.libX11
            xorg.libXext
            xorg.libSM
            xorg.libICE
            xorg.xcbutil
          ];
          QT_QPA_PLATFORM = "xcb";
          shellHook = ''
            if [ ! -d .venv ]; then
              ${py}/bin/python -m venv .venv
              cat >.venv/bin/py <<EOF
              LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH .venv/bin/python "\$@"
            EOF
              chmod +x .venv/bin/py
            fi
              . ./.venv/bin/activate
          '';
        };
      }
    );
}
