{ pkgs, lib, ... }:

{
  languages.python = {
    enable = true;
    package = pkgs.python312;

    venv = {
      enable = true;
      requirements = ./requirements.txt;
    };
  };

  packages = [
    pkgs.git
  ];

  enterShell = ''
    pip install -e . --quiet --disable-pip-version-check
  '';

  scripts.test.exec = ''
    python -m unittest discover -s tests -p "*_test.py" "$@"
  '';

  scripts.sqlaxe-cli.exec = ''
    python -m sqlaxe.sqlaxe "$@"
  '';

  enterTest = ''
    python -m unittest discover -s tests -p "*_test.py"
  '';
}
