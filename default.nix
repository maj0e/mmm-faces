{
    pkgs   ? import <nixpkgs> {},
    stdenv ? pkgs.stdenv,
    FaceRecPyPkgs ? pythonPackages: with pythonPackages; [
    numpy
    ipython
    #opencv4
    dlib
    tensorflow
    
    # Code qualitiy
    isort black flake8 pylint
    
    ],
    opencvGtk ? pkgs.opencv4.override ( old : { enableGtk2 = true; })
}:

rec {
    FaceRec = stdenv.mkDerivation {
    name = "FaceRec";
    version = "dev-0.1";
    buildInputs = with pkgs; [
      openblas
      opencvGtk
      dlib
      python37Packages.Nuitka
      clang
      (python3.withPackages FaceRecPyPkgs)
    ];
  };
}
