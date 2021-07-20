
const convertToPercentCrop = (crop, areaRef) =>{
	let imageWidth = areaRef.current ? areaRef.current.offsetWidth : 0
	let imageHeight = areaRef.current ? areaRef.current.offsetHeight : 0
	return _convertToPercentCrop(crop, imageWidth, imageHeight)
}
const convertToPixelCrop = (crop, areaRef) =>{
	let imageWidth = areaRef.current ? areaRef.current.offsetWidth : 0
	let imageHeight = areaRef.current ? areaRef.current.offsetHeight : 0
	return _convertToPixelCrop(crop, imageWidth, imageHeight)
}
const convertCropToTask = (crop, imageRef, areaRef) => {
	let naturalWidth = imageRef.current ? imageRef.current.naturalWidth : 0
	let naturalHeight = imageRef.current ? imageRef.current.naturalHeight : 0
	let crop_percentage = convertToPercentCrop(crop, areaRef)
	let x= Math.round((crop_percentage.x*naturalWidth)/100)
	let y= Math.round((crop_percentage.y*naturalHeight)/100)
	let width= Math.round((crop_percentage.width*naturalWidth)/100)
	let height= Math.round((crop_percentage.height*naturalHeight)/100)
	return {x: x, y:y, width: width, height: height}
}
const convertTaskToCrop = (task, imageRef, areaRef) => {
	let naturalWidth = imageRef.current ? imageRef.current.naturalWidth : 0
	let naturalHeight = imageRef.current ? imageRef.current.naturalHeight : 0
	let x= task.x/naturalWidth * 100
	let y= task.y/naturalHeight * 100
	let width= task.width/naturalWidth * 100
	let height= task.height/naturalHeight * 100

	return convertToPixelCrop({x: x, y:y, width: width, height: height, unit: "%"}, areaRef)
}
export {convertTaskToCrop as convertNaturalToCrop, convertCropToTask as convertCropToNatural, convertToPixelCrop, convertToPercentCrop}
//The following code is licensed under:
/*ISC License

Copyright (c) 2015, Dominic Tobias

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/
function _convertToPercentCrop(crop, imageWidth, imageHeight) {
	if (crop.unit === '%') {
		return crop;
	}

	return {
		unit: '%',
		aspect: crop.aspect,
		x: (crop.x / imageWidth) * 100,
		y: (crop.y / imageHeight) * 100,
		width: (crop.width / imageWidth) * 100,
		height: (crop.height / imageHeight) * 100,
	};
}

function _convertToPixelCrop(crop, imageWidth, imageHeight) {
	if (!crop.unit) {
		return { ...crop, unit: 'px' };
	}

	if (crop.unit === 'px') {
		return crop;
	}

	return {
		unit: 'px',
		aspect: crop.aspect,
		x: (crop.x * imageWidth) / 100,
		y: (crop.y * imageHeight) / 100,
		width: (crop.width * imageWidth) / 100,
		height: (crop.height * imageHeight) / 100,
	};
}
