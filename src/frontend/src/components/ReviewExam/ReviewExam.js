import Rectangle from "../Rectangle";
import {useRef, useState} from 'react'
import "../TaskSelector.css"
import TaskReviewingAreas from "./TaskReviewingAreas";
import "./ReviewExam.css"




function ReviewExam({exam, setExam, goBack}) {
	const [hoverIndex, setHoverIndex] = useState(-1)
	const [imageLoaded, setImageLoaded] = useState(false)
	const setTasks = (newTasks) => {
        let n = exam.clone()
		n.tasks = newTasks
        setExam(n)
    }

    const imageArea = useRef()
	let imageElementRef = useRef()


	let naturalWidth = imageElementRef.current ? imageElementRef.current.naturalWidth : 0
	let naturalHeight = imageElementRef.current ? imageElementRef.current.naturalHeight : 0

    let imageWidth = imageArea.current ? imageArea.current.offsetWidth : 0
    let imageHeight = imageArea.current ? imageArea.current.offsetHeight : 0
    function convertToPercentCrop(crop) {
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

    function convertToPixelCrop(crop) {
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




	const convertCropToNatural = (crop) => {
        let crop_percentage = convertToPercentCrop(crop)
		let x= Math.round((crop_percentage.x*naturalWidth)/100)
		let y= Math.round((crop_percentage.y*naturalHeight)/100)
		let width= Math.round((crop_percentage.width*naturalWidth)/100)
		let height= Math.round((crop_percentage.height*naturalHeight)/100)
		return {x: x, y:y, width: width, height: height}
	}
	const convertNaturalToCrop = (task) => {
		let x= naturalWidth ? task.x/naturalWidth * 100 : 0
		let y= naturalHeight ? task.y/naturalHeight * 100 : 0
		let width= naturalWidth ? task.width/naturalWidth * 100 : 0
		let height= naturalHeight ? task.height/naturalHeight * 100 : 0

		return convertToPixelCrop({x: x, y:y, width: width, height: height, unit: "%"})
	}
	const onHover = (index) =>{
		setHoverIndex(index)
	}

			
    return (
		<div className="TaskSelector">
			<div className={"column column-left"}>
				<div ref={imageArea} className="imageArea">
					<img ref={imageElementRef} alt={"Please select a file"} id="p1" src={exam.image} className="exame" onLoad={()=>{setImageLoaded(true)}}/>
					{imageLoaded && exam.tasks.map( (task, index) => {
						let crop = convertNaturalToCrop(task)
                        return(
                        <Rectangle
                        key={"rect" + index}
                        width={Math.round(crop.width)}
                        height={Math.round(crop.height)}
                        x={Math.round(crop.x)}
                        y={Math.round(crop.y)}
						className={hoverIndex === index ?" hover" : "no-hover"}
                        />
					)})}
				</div>
			</div>
				<button onClick={goBack}>
					Go Back
				</button>
			<div className={"column column-right"}>
					<TaskReviewingAreas tasks={exam.tasks} setTasks={setTasks} hover={onHover}/>
			</div>

        </div>)
}
export default ReviewExam;
