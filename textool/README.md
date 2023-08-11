## A Fork of a Fork
This version of Klei Studio is a fork of zxcvbnm3057's fork of the original. Their fork implements some nice quality-of-life improvements and fixes to the original that you can read about in its [history](https://github.com/zxcvbnm3057/dont-starve-tools/commits/master).

This fork extends that further with the following changes:
 - The fix that zxcvbnm3057 implemented for not being able to select individual elements in an atlas within TEXTool in locales that use decimal points as the fractional delimiter inadvertently broke the feature for user's in locales that use commas as the fractional delimiter. This version implements a locale agnostic fix.
 - Since the original, this tool has had an off-by-one issue when reading/writing a TEX file's texture type (1D, 2D, 3D or cube-mapped), and so it displayed the wrong type when reading a file and one had to select the option proceeding their actual selection (i.e. "1D" to create a 2D texture) when making a TEX file in TEXCreator; this also made creating true 1D textures impossible. This version fixes this problem.
 - TEXCreator will now actually set the true pitch value of mipmaps instead of just using 0. While TEXTool didn't rely on this value and just assumed the default pitch of image_width * 4, any tool that reads and uses the explicit pitch value instead of assuming the default would break since it was set to 0.
 - Fixes an off-by-one error when displaying atlas element dimensions that's been present since the original.

## Synopsis

Klei Studio is a simple suite of tools for Don't Starve (and can be used for their other games too).

Note: These tools are old and unmaintained and may contain bugs. You should really use the official tools instead.

## Quick start

* [Download the latest release](https://github.com/oblivioncth/dont-starve-tools/releases).

## Contributing

If you would like to contribute bug fixes and the likes, just make a pull request.

## Copyright and license

Copyright 2013-2020 Matt Stevens under [the MIT license](LICENSE).
