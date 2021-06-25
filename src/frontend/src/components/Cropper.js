import ReactCrop from 'react-image-crop';
import React from 'react'
import 'react-image-crop/dist/ReactCrop.css';
const Cropper = React.forwardRef(({component, crop, onChange, disabled}, ref) => ( 
		<div className={"croppingArea"} id="croppingArea" ref={ref}>
			<ReactCrop renderComponent={component} crop={crop} onChange={onChange} disabled={disabled} />
		</div>
	));
export default Cropper

