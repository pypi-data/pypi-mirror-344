# OpenSlide Python

OpenSlide Python is a Python interface to the OpenSlide library.

[OpenSlide] is a C library that provides a simple interface for reading
whole-slide images, also known as virtual slides, which are high-resolution
images used in digital pathology.  These images can occupy tens of gigabytes
when uncompressed, and so cannot be easily read using standard tools or
libraries, which are designed for images that can be comfortably
uncompressed into RAM.  Whole-slide images are typically multi-resolution;
OpenSlide allows reading a small amount of image data at the resolution
closest to a desired zoom level.

OpenSlide can read virtual slides in several formats:

* [Aperio][] (`.svs`, `.tif`)
* [DICOM][] (`.dcm`)
* [Hamamatsu][] (`.ndpi`, `.vms`, `.vmu`)
* [Leica][] (`.scn`)
* [MIRAX][] (`.mrxs`)
* [Philips][] (`.tiff`)
* [Sakura][] (`.svslide`)
* [Trestle][] (`.tif`)
* [Ventana][] (`.bif`, `.tif`)
* [Zeiss][] (`.czi`)
* [Generic tiled TIFF][] (`.tif`)

[OpenSlide]: https://openslide.org/
[Aperio]: https://openslide.org/formats/aperio/
[DICOM]: https://openslide.org/formats/dicom/
[Hamamatsu]: https://openslide.org/formats/hamamatsu/
[Leica]: https://openslide.org/formats/leica/
[MIRAX]: https://openslide.org/formats/mirax/
[Philips]: https://openslide.org/formats/philips/
[Sakura]: https://openslide.org/formats/sakura/
[Trestle]: https://openslide.org/formats/trestle/
[Ventana]: https://openslide.org/formats/ventana/
[Zeiss]: https://openslide.org/formats/zeiss/
[Generic tiled TIFF]: https://openslide.org/formats/generic-tiff/


## Requirements

* Python ≥ 3.9
* OpenSlide ≥ 3.4.0
* Pillow


## Installation

OpenSlide Python requires [OpenSlide].  Install both components from PyPI
with:

```console
pip install openslide-python openslide-bin
```

Or, see the [OpenSlide Python documentation][installing] for instructions on
installing so OpenSlide Python can find OpenSlide.

[installing]: https://openslide.org/api/python/#installing


## More Information

- [API documentation](https://openslide.org/api/python/)
- [Changelog](https://github.com/openslide/openslide-python/blob/main/CHANGELOG.md#notable-changes-in-openslide-python)
- [Website][OpenSlide]
- [GitHub](https://github.com/openslide/openslide-python)
- [Sample data](https://openslide.cs.cmu.edu/download/openslide-testdata/)


## License

OpenSlide Python is released under the terms of the [GNU Lesser General
Public License, version 2.1](https://openslide.org/license/).  The Deep Zoom
example code includes JavaScript released under the
[BSD license](https://github.com/openslide/openslide-python/tree/main/examples/deepzoom/licenses/LICENSE.openseadragon),
the
[MIT license](https://github.com/openslide/openslide-python/tree/main/examples/deepzoom/licenses/LICENSE.jquery),
and released into the
[public domain](https://github.com/openslide/openslide-python/tree/main/examples/deepzoom/licenses/LICENSE.openseadragon-scalebar).

OpenSlide Python is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
License for more details.
