# Stexatlaser (Stex)
<img align="left" src="https://i.imgur.com/LCBz647.png" width=25%>

Stexatlaser (*stex-atlaser*, a play on 'spectacular'), or simply Stex, is a simple tool for generating a (Klei) TEX format atlas and its key from a simple folder structure with no external dependencies required.

It uses an implementation of the MaxRects algorithm to efficiently pack each input element image into a larger atlas image, with as little wasted space as possible. Some empty space is inevitable given that atlases must have power-of-two dimensions.

It can also reverse the process and extract element images from an atlas using its key.


## Compatibility
While this tool was written with Don't Starve Together in mind, it should work with any Klei TEX file as long as the format is not significantly different. There are still a few unknowns concerning format interpretation with even DST, but they do not impact the performance of this tool and will be addressed in the event they're determined to be relevant.


## Usage
Stex uses the following syntax scheme:

    stex <global options> [command] <command options>
The order of switches within each options section does not matter.


### Basic Usage

**Creating an Atlas**
To create an atlas/key, start by setting up an input folder with the following structure:

    .atlas_name
    |-- element1_name.png
    |-- element2_name.png
    |-- element3_name.png
    |-- ...
The available input formats can vary between systems, but most common formats are supported. See **All Commands/Options** for more information.

As implied by the above, the folder name will be used as the atlas/key name, and the file names (**with the extension ".tex"**, see "Additional Information") of each image will be used as their respective element names. All sub-folders and other files will be ignored.

Then run Stex with the **pack** command:

    stex pack -i "X:\Path\To\Input\Directory" -o "X:\Path\To\Output\Directory"

When finished, the resultant atlas.tex and key.xml files will be placed in the specified output directory. You can then refer to each element by its name in LUA without concerning yourself where they actually were placed within the atlas.

If you want to see the element arrangement, try viewing the output with a [TEX viewer](https://github.com/oblivioncth/dont-starve-tools/releases/).

**Extracting an Atlas**
To extract an atlas, run Stex with the **unpack** command:
 
    stex unpack -i "X:\Path\To\Input\key.xml" -o "X:\Path\To\Output\Directory"

The key's corresponding atlas, which must be located alongside it, will be read automatically using the name specified within the key.

When finished, a subfolder with the name of the atlas will be created within the specified output directory that contains each individual element as a separate PNG image. This results in the same structure used as input when packing an atlas.


### Advance Usage
- If the alpha channel was **not** pre-multiplied when a given TEX atlas was created, the **-s** switch must be passed to **unpack** for the images to be recovered correctly. This is handled automatically for atlas/key pairs that were generated with Stex's pack command, as detailed in the "Additional Features" section 
- See the following section for more detailed options/modes.


## All Commands/Options
The recommended way to use all switches is to use their short form when the value for the switch has no spaces:

    -i C:/Users/Name/Desktop/input

and the long form when the value does have spaces

    --input="C:/Textures/Don't Starve Together/input.xml"
though this isn't required as long as quotation and space use is carefully employed.


### Global Options:
 -  **-h | --help | -?:** Prints usage information
 -  **-v | --version:** Prints the current version of the tool
 - **-f | --formats:** Prints the image formats supported by the tool (input only)
 
 
### Commands:
**pack** - Pack  a  folder  of  images  into  a  TEX  atlas.  The  input  directory  will  be  used  as  the  name  for  the  atlas/key, while  the  image  names  will  be  used  as  the  element  names

Options:
 -  **-i | --input:** Directory  containing  images  to  pack
 -  **-o | --output:** Directory  in  which  to  place  the  resultant  atlas  and  key
 -  **-f | --format:** Pixel  format  to  use  when  encoding  to  TEX.  The valid options are <dxt1 | dxt3 | dxt5 | rgb | rgba>. Defaults  to  DXT5
 -  **-u | --unoptimized:** Do  not  generate  smoothed  mipmaps
 -  **-s | --straight:** Keep  straight  alpha  channel,  do  not  pre-multiply
 - **-m | --margin:** Add  a  1-px  transparent  margin  to  each  input  image  (when  more  than  one).  Useful  for  rare  cases  of  element  bleed-over

Requires:
**-i** and **-o** 

Notes: 
Use `stex -f` to see the supported image formats. The **margin** switch is generally never required and is only available for extremely specific and unlikely cases in which floating point inaccuracies or rounding cause 1 row/column of pixels from one element to be marked as part of another during atlas key generation. 

--------------------------------------------------------------------------------

**unpack** - Unpack  a  TEX  atlas  into  its  component  images in PNG format

Options:
 -  **-i | --input:** Key  of  the  atlas  to  unpack.  Must  be  in  the  same  directory  as  its  atlas
 -  **-o | --output:** Directory  in  which  to  place  the  resultant  folder  of  unpacked  images
 -  **-s | --straight:** Specify  that  the  alpha  information  within  the  input  TEX  is  straight,  do  not  de-multiply

Requires:
**-i** and **-o** 

Notes: 
Because Klei TEX atlas keys use relative coordinates and converting to/from them incurs floating-point inaccuracies, there are some edge cases where the dimensions of unpacked images may differ very slightly from the originals used to create the TEX; however, this is generally not the case.

Still, for this reason it is recommended to keep original copies of your textures and not rely on the TEX version as your only copy.

--------------------------------------------------------------------------------
 
## Additional Information
**Automatic Pre-multiplied Alpha Handling**

A small shortcoming of the TEX format is that it doesn't store whether or not its image data is using pre-multiplied alpha (unless that's the purpose of one of the two unknown flags), and so one needs to somehow otherwise know if this is the case and manually specify that the alpha needs to be de-multiplied when using tools that handle TEX files (they often just assume they need to). To circumvent this, any TEX atlases created with Stex's **pack** command will have an extra entry in their key that records this property. This value is then subsequently read and utilized when extracting that same TEX using Stex's **unpack** command. If the value isn't present within a key then an input atlas is assumed to be using pre-multiplied alpha unless the **-s** switch is used with the unpack command.

Simply put, if you always pack and unpack your multi-image atlases with Stex you will never have to worry about this.

Although this breaks the "standard" for atlas keys, since they are just XML files the game's parser will simply ignore this extra element and it therefore causes no issues and maintains compatibility.

**Atlas Key Element Extensions**

Although in a practical sense they shouldn't be needed, some atlas elements require the extension ".tex" to function properly due to the exact implementation of some Klei scripts. The elements themselves don't actually refer to files and instead are just labels for the images within a TEX file, which makes this requirement a bit award and sometimes confusing, but nonetheless Stex ensures compliance with this annoyance. Any input images that don't already end with ".tex" (before their actual extension) will have the extension appended to the element name that their filename becomes.

*Example:*
| Image Filename    | Resultant Element Name |
|-------------------|------------------------|
| texture01.tex.png | texture01.tex          |
| texture02.png     | texture02.tex          |

This extension will be removed during filename assignment when unpacking an atlas.

## Source

### Summary

 - C++20
 - CMake 3.23.0
 - Targets:
	 - Windows 10+
	 - Linux

### Dependencies
- Qt6
- [Qx](https://github.com/oblivioncth/Qx/)
- [libsquish](https://sourceforge.net/projects/libsquish/)
- [OBCMake](https://github.com/oblivioncth/OBCmake)

## Pre-built Releases/Artifacts

Releases and some workflows currently provide builds of Stex in various combinations of platforms and compilers. View the repository [Actions](https://github.com/oblivioncth/Stexatlaser/actions) or [Releases](https://github.com/oblivioncth/Stexatlaser/releases) to see examples

### Details
The source for this project is managed by a sensible CMake configuration that allows for straightforward compilation and consumption of its target(s), either as a sub-project or as an imported package. All required dependencies except for Qt6 are automatically acquired via CMake's FetchContent mechanism.

## Klei TEX Format
When creating this tool I couldn't find any documentation on the Klei TEX format and had to use other existing tools' code as reference. I have provided my interpretation here for convenience:

    KTEX FORMAT
    ============
    0x00 - HEADER (pre or post caves update)
    0x08 - MIMAP_METADATA[Mipmap_Count]
    0x^^ - MIMAP_DATA[Mipmap_Count]
    
    HEADER (pre-caves update)
    ------
    0x00 - uint8[4]: Magic Number "KTEX"
    0x04 - uint32: Specifications
    >> Specifications
       --------------
       b0:2 - uint3: Platform
       b3:5 - uint3: Pixel Format
       b6:8 - uint3: Texture Type
       b9:12 - uint4: Mipmap Count
       b13 - uint1: Flags (Unknown)
       b14:31 - uint18: *padding (all high)*
       
    HEADER (post-caves update)
    ------
    0x00 - uint8[4]: Magic Number "KTEX"
    0x04 - uint32: Specifications
    >> Specifications
       --------------
       b0:3 - uint4: Platform
       b4:8 - uint5: Pixel Format
       b9:12 - uint4: Texture Type
       b13:17 - uint5: Mipmap Count
       b18:19 - uint2: Flags (Unknown)
       b20:31 - uint12: *padding (all high)*
       
    MIPMAP_METADATA
    ---------------
    0x00 - uint16: Width
    0x02 - uint16: Height
    0x04 - uint16: Pitch
    0x06 - uint32: Data Size
    
    MIMAP_DATA
    ----------
    0x00 - uint8[Data_Size]: Image Data

This tool defaults both flags in the newer header spec (the only one used when writing) to high. If anyone knows the purpose of these flags I'd be grateful if you could share it with me.
