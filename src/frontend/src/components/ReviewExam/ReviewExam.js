import Rectangle from "../Rectangle"
import {React, useRef, useState} from 'react'
import "../TaskSelector.css"
import TaskReviewingAreas from "./TaskReviewingAreas"
import "./ReviewExam.css"
import {convertNaturalToCrop as _convertNaturalToCrop} from '../CropConverter'



function ReviewExam({exam, setExam, goBack}) {
	const [hoverIndex, setHoverIndex] = useState(-1)
	const [imageLoaded, setImageLoaded] = useState(false)
	const setTasks = (newTasks) => {
		let newExam = exam.clone()
		newExam.tasks = newTasks
		setExam(newExam)
	}

	const imageArea = useRef()
	const imageElementRef = useRef()
	const convertNaturalToCrop = (crop) =>{
		return _convertNaturalToCrop(crop, imageElementRef, imageArea)
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
				<TaskReviewingAreas tasks={exam.tasks} setTasks={setTasks} setHoverIndex={setHoverIndex}/>
			</div>

		</div>)
}
export default ReviewExam
