with import <nixpkgs> { };

let
  pythonPackages = python312Packages;
in pkgs.mkShell rec {
    name = "impurePythonEnv";
    venvDir = "./.venv";
    buildInputs = [
        pythonPackages.python
        pythonPackages.venvShellHook
        pythonPackages.psycopg2
    ];

    postVenvCreation = ''
        unset SOURCE_DATE_EPOCH
        pip install -e .
    '';

    postShellHook = ''
        # allow pip to install wheels
        unset SOURCE_DATE_EPOCH
    '';
}
