import Cropper from "./components/Cropper";
import Tasks from "./components/Tasks";
import Rectangle from "./components/Rectangle";
import "cropperjs/dist/cropper.css";
import {useState} from 'react'
import exame from './pics/exame.jpg'
import './App.css'



let defaultTaskType = 'text'

function App() {
    const [crop, setCrop] = useState({});
    const [taskList, setTaskList] = useState({tasks: [], i: 0})
    const [editing, setEditing] = useState(false)
	const [submitText, setSubmitText] = useState("")
	const [image, setImage] = useState(exame)
	const [exams, setExams] = useState([])
	let imageElement = (
		<img alt={image ? "An Site of an exame": "Please select a image"} id="p1" src={image} className="exame"/>
	)

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
					return {...task, crop: crop}
				} else {
                    return task
                }
            }
        )
        setTaskList({...taskList, tasks: newTasks})
        setCrop({...crop, x: 0, y: 0, width: 0, height: 0})
    }


    let AddOnClick = () => {
		saveCropInNewTask(crop)
    }
    let IsAddEnabled = () => {
		return crop.width>0&&crop.height>0&&!editing
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
							return {
								x: task.crop.x,
								y: task.crop.y,
								height: task.crop.height,
								width: task.crop.width,
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
			.then( (json) => {setSubmitText("Successful"); console.log(json)} )
			.catch( (err) => {console.error("Something went wrong while sending to backend. \n" + err); setSubmitText("Failed :/")} )
	}


    return (
		<div className="App">
			<div className={"column column-left"}>
				<input type="file" accept="image/*,application/pdf" onChange={onSelectFile} />
				<div className="imageArea">
					{taskList.tasks.map(
						(task) => <Rectangle key={"rect" + task.id} width={task.crop.width} height={task.crop.height} x={task.crop.x} y={task.crop.y} />
					)}
					<Cropper
						disabled={false}
						crop={crop}
						component={imageElement}
						onChange={newCrop => setCrop(newCrop)}
						onConplete={newCrop => setCrop(newCrop)}
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

export default App;
