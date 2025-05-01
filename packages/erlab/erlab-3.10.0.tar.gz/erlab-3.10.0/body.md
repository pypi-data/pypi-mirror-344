## v3.10.0 (2025-05-01)

### ✨ Features

- **dtool:** add `fillna()` to generated code for input data with missing values ([fc1ad89](https://github.com/kmnhan/erlabpy/commit/fc1ad89d522ebd9d34a8a710b36b1e79abeaa657))

- **imagetool:** add IPython magic commands for ImageTool integration ([470e0b4](https://github.com/kmnhan/erlabpy/commit/470e0b46cbec7e8f3edd1a2329abeeeb76b76c9d))

  Adds a new IPython magic command `%itool` for convenient integration of ImageTool with IPython and Jupyter notebooks. Load the extension using `%load_ext erlab.interactive` and run `%itool?` to see available commands.

- **imagetool:** enable directly opening tools with cropped data ([d6bf78a](https://github.com/kmnhan/erlabpy/commit/d6bf78ae4673ea35dd1f250c924e2a1e4a79b064))

  A new feature has been added to the imagetool that allows users to open the tool with cropped data directly. When holding down the Alt key (Option on Mac) while in the right-click menu of the image, relevant menus will automatically work with the data cropped to the currently visible range.

- **explorer:** show the name of the current directory in data explorer ([7262b4c](https://github.com/kmnhan/erlabpy/commit/7262b4c6cb5f7a461a108eca8bc11d95a9e35531))

- **imagetool:** add edge correction menu ([fb47f1b](https://github.com/kmnhan/erlabpy/commit/fb47f1b23889030d8f4ae61455284af26530e137))

  Adds a new menu item that allows correcting the Fermi edge by loading a polynomial fit result from a file saved from `goldtool`.

- **goldtool:** add button to save polynomial fit to file ([94422b1](https://github.com/kmnhan/erlabpy/commit/94422b1429ae61ef4d250ffe0d74cd1a7a5dc5c2))

- **interactive.utils:** add functions for saving and loading fit results from the GUI ([30caff2](https://github.com/kmnhan/erlabpy/commit/30caff28f2c82b1dd6eb82092fe9338390e3f4a4))

### 🐞 Bug Fixes

- **imagetool:** fix centered normalization and reverse colormap not being applied when loading or unarchiving ([5626509](https://github.com/kmnhan/erlabpy/commit/56265093b0561ecd49b6801d88171b4b0a050155))

- **imagetool:** resolve undesired y axis autoscaling of line plots when resizing unrelated axes ([a089c8b](https://github.com/kmnhan/erlabpy/commit/a089c8bb29b2f3a994ecff36b30b190d53670e9f))

- **imagetool:** resolve associated coords not updating on data reload ([66c44f5](https://github.com/kmnhan/erlabpy/commit/66c44f5b3c6591a1771551e3d50b1eb24ff95f5a))

  Fixes associated coordinates limits not being updated when the data is reloaded.

- **plotting:** fix color limits not being autoscaled when passing an iterable of norms to `plot_slices` ([fbfd3ec](https://github.com/kmnhan/erlabpy/commit/fbfd3ec41a807a01d685c00c9f5b9a1f7ad7e514))

### ⚡️ Performance

- **goldtool:** do not apply correction if not required ([6276883](https://github.com/kmnhan/erlabpy/commit/6276883b1fc78b50fac4ec6b481fff5ae490095c))

  Greatly improves the performance of spline and polynomial fitting in goldtool by correcting data just in time.

### ♻️ Code Refactor

- **imagetool:** improve error messages for invalid input ([90d3461](https://github.com/kmnhan/erlabpy/commit/90d34612d6969d3cd69f97202d6eb6e9370daa97))

- **manager:** add internal function to retreive recent directory (intraprocess only) ([5d5cf96](https://github.com/kmnhan/erlabpy/commit/5d5cf96fec86c0917c0718d2cd1225787ded202e))

[main a38b330] bump: version 3.9.0 → 3.10.0
 3 files changed, 23 insertions(+), 3 deletions(-)

