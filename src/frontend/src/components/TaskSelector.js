import Cropper from "./Cropper";
import Tasks from "./Tasks";
import Rectangle from "./Rectangle";
import "cropperjs/dist/cropper.css";
import {useRef, useState} from 'react'
import exame from '../pics/exame.jpg'
import './TaskSelector.css'



let defaultTaskType = 'text'

function TaskSelector() {
    const [crop, setCrop] = useState({});
    const [crop_percentage, setCrop_percentage] = useState({"width":0, "height":0, "unit": "%"});
    const [taskList, setTaskList] = useState({tasks: [], i: 0})
    const [editing, setEditing] = useState(false)
	const [submitText, setSubmitText] = useState("")
	const [image, setImage] = useState(exame)
	const [exams, setExams] = useState([])
    const croppingArea = useRef()
	let imageElementRef = useRef()
	let imageElement = (
		<img ref={imageElementRef} alt={image ? "An Site of an exame": "Please select a image"} id="p1" src={image} className="exame"/>
	)
	let naturalWidth = imageElementRef.current ? imageElementRef.current.naturalWidth : 0
	let naturalHeight = imageElementRef.current ? imageElementRef.current.naturalHeight : 0

    let imageWidth = croppingArea.current ? croppingArea.current.offsetWidth : 0
    let imageHeight = croppingArea.current ? croppingArea.current.offsetHeight : 0

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

	let setTasks = (tasks) => {
		setTaskList({...taskList, tasks: tasks})
	}

    let load = (task) => {
        setCrop(task.crop)
    }

    let del = (id) => {
        let newTasks = taskList.tasks.filter((task) => task.id !== id)
        setTaskList({...taskList, tasks: newTasks})
    }

	let saveCropInNewTask = (crop) => {
		let newTask = {id: taskList.i, crop:crop, type:defaultTaskType, expected: ""}
        setTaskList({i: taskList.i + 1, tasks: [...taskList.tasks, newTask]})
        setCrop({...crop, x: 0, y: 0, width: 0, height: 0})
    }
    let saveCropInExistingTask = (new_task) => {
        let newTasks = taskList.tasks.map((task) => {
                if (task.id === new_task.id) {
					return {...task, crop: crop_percentage}
				} else {
                    return task
                }
            }
        )
        setTaskList({...taskList, tasks: newTasks})
        setCrop({...crop_percentage, x: 0, y: 0, width: 0, height: 0})
    }


    let AddOnClick = () => {
		saveCropInNewTask(crop_percentage)
    }
    let IsAddEnabled = () => {
		return crop_percentage.width>0&&crop_percentage.height>0&&!editing
	}
    const setPdfAsImage = (pdf) => {
		fetch("/web-backend/pdf2img/", 
            {
				method: 'POST',
				headers:{
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ pdf:pdf })
			}
        )
        .then( res => {
            if(!res.ok){
                throw new Error( `Backend responses: ${res.status}`)
            }
            return res.json()
        })
		.then((json)=> { setImage(json.img) })
		.catch( (err) => {
			console.log("that didnt work" + err);
			alert("Beim Konvertieren ist leider etwas schief gegangen :/")
		})
    }
	
	const onSelectFile = (e) => {
		if (e.target.files && e.target.files.length > 0) {
			let file = e.target.files[0]
			if (file.type === "application/pdf"){
                //convert
                const reader = new FileReader();
                reader.addEventListener('load', () => setPdfAsImage(reader.result));
                reader.readAsDataURL(file);
			}else{
				const reader = new FileReader();
				reader.addEventListener('load', () => setImage(reader.result));
				reader.readAsDataURL(file);
			}
		}
	}

	const onSelectExams = (e) => {
		let files = [...e.target.files]
		let newExams = []
		files.forEach( (file) => {
			const reader = new FileReader();
			reader.addEventListener('load', () => newExams.push(reader.result));
			reader.readAsDataURL(file);
		})
		setExams(newExams)
	}
	

	function sendToBackend(){
		fetch("/web-backend/", 
			{
				method: 'POST',
				headers:{
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(
					{
						tasks: taskList.tasks.map((task) => {
                            // console.log(task);
							console.log(task.crop.width)
							console.log(naturalWidth)
							return {
								x: Math.round((task.crop.x*naturalWidth)/100),
								y: Math.round((task.crop.y*naturalHeight)/100),
								height: Math.round((task.crop.height*naturalHeight)/100),
								width: Math.round((task.crop.width*naturalWidth)/100),
								type: task.type,
								expected: task.expected,

							}
						}),
						img: image,
						exams: exams
					}
				)
			})
			.then( res => {
				if(!res.ok){
					setSubmitText("Failed to reach the Backend")
					throw new Error( `Backend responses: ${res.status}`)
				}
				return res.json()
					
			})
            .then( (json) => {setSubmitText("Successful"); console.log(json); alert(JSON.stringify(json.tasks))} )
			.catch( (err) => {console.error("Something went wrong while sending to backend. \n" + err); setSubmitText("Failed :/")} )
	}

    

    return (
		<div className="TaskSelector">
			<div className={"column column-left"}>
				<input type="file" accept="image/*,application/pdf" onChange={onSelectFile} />
				<div className="imageArea">
					{taskList.tasks.map( (task) => {
                        task.crop_px = convertToPixelCrop(task.crop)
                        return(
                        <Rectangle
                        key={"rect" + task.id}
                        width={task.crop_px.width}
                        height={task.crop_px.height}
                        x={task.crop_px.x}
                        y={task.crop_px.y}
                        />
					)})}
					<Cropper
						disabled={false}
						crop={crop}
						component={imageElement}
						onChange={(newCrop_px, newCrop_percentage)=> {setCrop(newCrop_px); setCrop_percentage(newCrop_percentage)}}
                        ref={croppingArea}
					/>
				</div>
			</div>
			<div className={"column column-right"}>
				<button onClick={() => AddOnClick()} disabled={!IsAddEnabled()}>Add</button>
				<Tasks tasks={taskList.tasks} setTasks={setTasks} load={load} del={del} save={saveCropInExistingTask} editing={editing} setEditing={setEditing}/>
				Select documents to correct<br/>
				<input type="file" accept="image/*,application/pdf" multiple="multiple" onChange={onSelectExams}/>
				{taskList.tasks.length>0 && <div><button onClick={sendToBackend} >Submit</button><pre>{submitText}</pre></div>}
            </div>

        </div>
    );
}

export default TaskSelector;
