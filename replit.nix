{ pkgs }: 

pkgs.mkShell {
  buildInputs = [
    pkgs.python39Full       # Python 3.9 (ou adapte selon version)
    pkgs.python39Packages.fastapi
    pkgs.python39Packages.uvicorn
  ];

  shellHook = ''
    echo "Environnement prêt pour FastAPI avec Uvicorn"
  '';
}
