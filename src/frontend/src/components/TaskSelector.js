import Cropper from "./Cropper";
import TaskEditingAreas from "./TaskEditingAreas";
import Rectangle from "./Rectangle";
import {useRef, useState} from 'react'
import './TaskSelector.css'
import {ExamContainer, Task} from "./ExamContainer"




function TaskSelector({exam, setExam, examContainer, setExamContainer, setStudentExams, leave}) {
	const [reviewing, setReviewing] = useState(false)
	const [hoverIndex, setHoverIndex] = useState(-1)

    const [crop, setCrop] = useState({});
    const resetCrop = () =>{
    	setCrop({...crop, x:0, y: 0, width: 0, height: 0})
	}
    const [editing, setEditing] = useState(false)
	const [submitText, setSubmitText] = useState("")

	const setTasks = (newTasks) => {
        let n = exam.clone()
		n.tasks = newTasks
        setExam(n)
    }

    const croppingArea = useRef()
	let imageElementRef = useRef()


	let imageElement = (
		<img ref={imageElementRef} alt={"Correct Exam"} id="p1" src={exam.image} className="exame"/>
	)
	let naturalWidth = imageElementRef.current ? imageElementRef.current.naturalWidth : 0
	let naturalHeight = imageElementRef.current ? imageElementRef.current.naturalHeight : 0

    let imageWidth = croppingArea.current ? croppingArea.current.offsetWidth : 0
    let imageHeight = croppingArea.current ? croppingArea.current.offsetHeight : 0
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


    let loadTaskInCroppingArea = (index) => {
        setCrop(convertNaturalToCrop(exam.tasks[index]))
    }

    let deleteTask = (index) => {
        let n = exam.clone().tasks
        n=n.filter(item => item !== exam.tasks[index])
        setTasks(n)
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
		let x= task.x/naturalWidth * 100
		let y= task.y/naturalHeight * 100
		let width= task.width/naturalWidth * 100
		let height= task.height/naturalHeight * 100

		return convertToPixelCrop({x: x, y:y, width: width, height: height, unit: "%"})
	}
	let saveCropInNewTask = (crop) => {
		let a = convertCropToNatural(crop)
		let task = new Task(a.x, a.y, a.width, a.height)
		let n = exam.clone().tasks
		n.push(task)
        setTasks(n)
        resetCrop()
    }

    let saveCropInExistingTask = (index, crop) => {
		let n = exam.clone().tasks
        let task = n[index]
		let {x, y, width, height} = convertCropToNatural(crop)
        task.x = x
		task.y = y
		task.width = width
		task.height = height
        n[index] = task
        setTasks(n)
		resetCrop()
    }


    let AddOnClick = () => {
		saveCropInNewTask(crop)
		resetCrop()
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
		.then((json)=> { setExamImage(json.img) })
		.catch( (err) => {
			console.log("that didnt work" + err);
			alert("Beim Konvertieren ist leider etwas schief gegangen :/")
		})
    }
    const setExamImage = ( image ) => {
        let n = exam.clone()
		n.image = image
		setExam(n)
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
				reader.addEventListener('load', () => setExamImage(reader.result));
				reader.readAsDataURL(file);
			}
		}
	}


	const handleFileChosen = async (file) => {
	  return new Promise((resolve, reject) => {
		let fileReader = new FileReader();
		fileReader.onload = () => {
		  resolve(fileReader.result);
		};
		fileReader.onerror = reject;
		fileReader.readAsDataURL(file);
	  });
	}
			
	const onSelectExams = async (e) => {
		let files = [...e.target.files]
		const results = await Promise.all( files.map( async (file) => {
			const fileContents = await handleFileChosen(file);
			return fileContents;
		}) )
        let filenames = files.map((file)=>{
        	return file.name
		})
		setStudentExams(results, filenames)
	}
	
	async function sendToBackend(){
    	setSubmitText("...")
		let response = await fetch("/web-backend/analyze_correct_exam/",
			{
				method: 'POST',
				headers:{
					'Content-Type': 'application/json'
				},
                body: JSON.stringify(examContainer)
			})
		if(!response.ok){
			setSubmitText("failed to reach the backend")
		}
		let examContainer_json = await response.json()
        setSubmitText("Successful")
        setExamContainer(ExamContainer.fromJSON(examContainer_json))
		setReviewing(true)
	}

    async function btn_next(){

    	setSubmitText("...")
		let response = await fetch("/web-backend/analyze_student_exams/",
			{
				method: 'POST',
				headers:{
					'Content-Type': 'application/json'
				},
                body: JSON.stringify(examContainer)
			})
		if(!response.ok){
			setSubmitText("failed to reach the backend")
		}
		let examContainer_json = await response.json()
        setSubmitText("Successful")
        setExamContainer(ExamContainer.fromJSON(examContainer_json))
        leave()
    }


    

    return (
		<div className="TaskSelector">
			<div className={"column column-left"}>
				<input type="file" accept="image/*,application/pdf" onChange={onSelectFile} />
				<div className="imageArea">
					{exam.tasks.map( (task, index) => {
						let crop = convertNaturalToCrop(task)
                        return(
                        <Rectangle
                        key={"rect" + index}
                        width={crop.width}
                        height={crop.height}
                        x={crop.x}
                        y={crop.y}
						className={hoverIndex === index ?" hover" : "no-hover"}
                        />
					)})}
					{examContainer.correctExam.image
						? <Cropper
							disabled={false}
							crop={crop}
							component={imageElement}
							onChange={(newCrop_px)=> {setCrop(newCrop_px)}}
							ref={croppingArea}
						/>
						: <div>Pleas select the corrected Exam from your computer</div>
					}
				</div>
			</div>
            {examContainer.correctExam.image &&
                <div className={"column column-right"}>
				<button onClick={() => AddOnClick()} disabled={!IsAddEnabled()}>Add</button>
				<TaskEditingAreas tasks={exam.tasks} setTasks={setTasks} loadCroppingArea={loadTaskInCroppingArea} deleteTask={deleteTask} saveCropInTask={(index) => {saveCropInExistingTask(index, crop)}} editing={editing} setEditing={setEditing} canEditAnswer={reviewing} setHoverIndex={setHoverIndex}/>
				{exam.tasks.length>0 && !reviewing && <div>
                    <button onClick={sendToBackend} >Submit</button><pre>{submitText}</pre>
                </div>}
					{reviewing && <div>
                        select documents to correct<br/>
                        <input type="file" accept="image/*,application/pdf" multiple="multiple" onChange={onSelectExams}/>
                    </div>
                }
				{reviewing && examContainer.studentExams.length > 0 && <button onClick={btn_next}>Next</button>}
            </div>}

        </div>
    );
}

export default TaskSelector;
