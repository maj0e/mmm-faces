 
let pkgs = import <nixpkgs> {
        config = {};
        overlays = [];
    };
    pkgsArm = import <nixpkgs> {
        config = {};
        overlays = [];
        system = "aarch64-linux";
    };
    pkgsCross = import <nixpkgs> {
        config = {};
        overlays = [
            (self: super: {
                hdf5 = pkgsArm.hdf5;
                gfortran = pkgsArm.gfortran;
                openmpi = pkgsArm.openmpi;
                lcms2 = pkgsArm.lcms2;
                gdk-pixbuf = pkgsArm.gdk-pixbuf;
            })
        ];
        crossSystem = pkgs.lib.systems.examples.aarch64-multiplatform;
    };
    opencvCross = pkgsCross.opencv4.override(old : {enableGtk2 = true;
  					    enablePNG= false;
  					    enableTIFF = false;
  					    enableContrib = false;
  					    enablePython = true; });
in
    pkgs.mkShell {
     buildInputs = [ pkgsCross.dlib pkgsCross.python37Packages.tensorflow ];#pkgsCross.python37Packages.tensorflow ];##pkgsCross.dlib ];
    }
