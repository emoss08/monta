#!/usr/bin/env bash
: '
COPYRIGHT 2022 MONTA

This file is part of Monta.

Monta is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Monta is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Monta.  If not, see <https://www.gnu.org/licenses/>.

-------------------------------------------------------------------------------

This script is used to convert static image files to AVIF format.
'

# Build avifenc command from git
sudo apt-get install zlib1g-dev
sudo apt-get install libpng-dev
sudo apt-get install libjpeg-dev

# Clone the repo
git clone -b v0.9.1 https://github.com/AOMediaCodec/libavif.git
cd libavif || exit

cd ext || exit
./aom.cmd
cd ..

mkdir build
cd build || exit
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=0 -DAVIF_CODEC_AOM=1 -DAVIF_LOCAL_AOM=1 -DAVIF_BUILD_APPS=1 ..
make

# Output directory to save AVIF images
output_dir="$1/avif"

# Convert all images in the directory to AVIF format
for file in "$1"/*; do
  if [ -f "$file" ]; then
    # Get the file name without extension
    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"

    # Convert the image to AVIF format
    echo "Converting $file to $output_dir/$filename.avif"
    ./avifenc "$file" "$output_dir/$filename.avif" --min 0 --max 63 --minalpha 0 --maxalpha 63 -a end-usage=q -a cq-level=18 -a tune=ssim
  fi
done
