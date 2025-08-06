# let
#   nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-unstable";
#   pkgs = import nixpkgs {
#     config = {};
#     overlays = [];
#   };
# in
with import <nixpkgs> {
  config = {};
  overlays = [];
};
  pkgs.mkShellNoCC {
    packages = with pkgs; [
      figlet
      lolcat
      python3Packages.requests
      python3Packages.aiohttp
    ];

    GREETING = "CHECK Xtream code";
    shellHook = ''
      figlet -t -f banner3-D $GREETING | lolcat
      echo "run command 'python main.py'"
      python async_main.py
    '';
  }
