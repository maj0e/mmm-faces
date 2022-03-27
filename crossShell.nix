

#with import <nixpkgs> {
  let pkgsArm = import <nixpkgs> {
    config = {};
    system = "aarch64-linux";
  };
  pkgsCross = import <nixpkgs> {
    config =  "aarch64-unknown-linux-gnu";
    overlays = [
      (self: super: {
        hdf5 = pkgsArm.hdf5;
      })
    ];
  };
  opencvCross = pkgsCross.opencv4.override(old : {enableGtk2 = true;
  					    enablePNG= false;
  					    enableTIFF = false;
  					    enableContrib = false; });
  in
  pkgsCross.mkShell {
    buildInputs = [ opencvCross pkgsCross.dlib ]; # your dependencies here
  }
                      
