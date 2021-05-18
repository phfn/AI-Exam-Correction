import {useState} from 'react'
const Task = ({task, setTask, load, del, save, editing, setEditing}) => {

	let [edit_mode, set_edit_mode] = useState(true)
	let [btn_edit_text, set_btn_edit_text] = useState("Edit")
	let btn_click = () => {
	    set_edit_mode(!edit_mode)
		setEditing(edit_mode)
		if(edit_mode){
			load(task)
            set_btn_edit_text("Save")
		}else{
			save(task)
            set_btn_edit_text("Edit")
		}
	}
	let setType = (type) => {
		setTask({...task, type:type})
	}
	let setExpected = (expected) => {
		setTask({...task, expected:expected})
	}
	const onSelectionChange = (event) => {
		let option = options.filter(option => option.value === event.target.value)[0]
		setTask({...task, type: option.value, expected: option.default})
	} 
	const options = [
		{ value: 'text', label: 'Text' , default: ""},
		{ value: 'checkbox', label: 'Single Choice Checkbox', default: '0' },
		]
	return(
	<div className={"task"}>
		<div className="buttons" key={"task-buttons"+task.id}>
			<button onClick={() => del(task.id)} disabled={editing}>Delete</button>
			<button onClick={() => btn_click()} disabled={editing&&edit_mode}>{btn_edit_text}</button>
		</div>

		<div className="form" key={"task-form-div"+task.id}>	
			<form className={"taskform"}>
				<div className={"type_selector"} key={"type_selector"+task.id}>
					<label htmlFor="type_selector">Aufgabentyp: </label>
					<select name="type_selector" onChange={onSelectionChange} value={task.type}>
						{options.map( (option) => {
							return(
								<option
									value={option.value}
									key={`${task.id}_${option.value}`}
									onChange={(event) => setType(event.state.value)}
								>
									{option.label}
								</option>
							)
						})}
					</select>

				</div>
				<div className={"text_awnser"} key={"text_awnser"+task.id}>
					{task.type === "text" &&
					<div/* key={"text_awnser text"+task.id}*/>
						<label htmlFor="text_awnser">Wie lautet die richtige Antwort: </label>
						<input type="text" name="text_awnser" min="0" value={task.expected} onChange={ (e) => {setExpected(e.target.value)} }/>
					</div>
					}
					{task.type === "checkbox" &&
					<div /*key={"text_awnser checkbox"+task.id}*/>
						<label htmlFor="checkbox_awnser">Welche Checkbox ist richtig: </label>
						<input type="number" min="0" name="checkbox_awnser" value={task.expected} onChange={ (e) => {setExpected(e.target.value)} }/>
					</div>
					}
				</div>
			</form>

		</div>
			

	</div>
	)
}
export default Task
