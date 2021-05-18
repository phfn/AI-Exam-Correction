import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';
function Cropper({component, crop, onConplete, onChange, disabled}) {

	return ( 
		<div className={"croppingArea"}>
			<ReactCrop renderComponent={component} crop={crop} onChange={onChange} onComplete={() => onConplete(crop)} disabled={disabled} />
		</div>
	)
}
export default Cropper

