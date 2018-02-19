# GWA Toolbox Installer <img src="https://github.com/DHI-GRAS/GWA_Installer/blob/master/GWA.ico" height="40">

This installer is part of The GWA toolbox developed under the GlobWetland Africa project. 

GlobWetland Africa (GWA) is a large Earth Observation application project funded by the European Space Agency (ESA) in partnership with
the African Team of the Ramsar convention on wetlands. The project is initiated to facilitate the exploitation of satellite observations
for the conservation, wise-use and effective management of wetlands in Africa and to provide African stakeholders with the necessary Earth
Observation (EO) methods and tools to better fulfil their commitments and obligations towards the Ramsar Convention on Wetlands. 

It calls the installers of the various software components (OSGeo4W software, BEAM, Snap Toolbox etc.) in the appropriate order and takes
care of post-installation tasks such as file copying (e.g. of QGIS plugins) or changing settings.

This is not the complete  software package. The actual software can be downloaded (after registration) at www.globwetland-africa.org.

## Uninstalling existing installations of WOIS or GWA Toolbox

For thoroughly uninstalling, please

1.	Delete `C:\OSGeo4W64`
2.	Start `regedit` (type in Windows search) and delete the folder `HKEY_CURRENT_USER\Software\QGIS`
3.	Unless you are updating from a very recent GWA installer, uninstall old versions of R, Postgres, PostGis, and SNAP (BEAM is not updated anymore, so you can leave that)
4.	Remove the `.qgis2` folder in your user directory `C:\Users\<username>\.qgis2` - NB: This may contain user data you want to save, so consider making a backup

## Updating existing installations

If you have a recent installation of the GWA Toolbox, you can choose to update only parts of the package. Click `Skip` on the steps of the installer that you think you do not need and `Continue` on the others. Always run the post-installation steps (for OSGeo4w, BEAM, SNAP, R, etc.), as these update scrips, workflows and the settings in QGIS.

Copyright (C) 2018 GlobWetland Africa (www.globwetland-africa.org) 


## Building

Building the installer requires pyqt version 4. Install it in Anaconda with `conda install pyqt=4`.
