{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.poetryPlugins.poetry-plugin-export
  ];


  # https://devenv.sh/languages/
  languages = {
    go.enable = true;
    python = {
      enable = true;
      version = "3.12";
      poetry = {
        enable = true;
        activate.enable = true;
      };
    };
  };

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
