import { React, useState } from "react"
const TaskEditingArea = ({
	task,
	taskId,
	setTask,
	loadCroppingArea,
	deleteTask,
	saveCropInTask,
	editing,
	setEditing,
	canEditAnswer,
	onHover,
	onHoverLeave,
}) => {
	const [edit_mode, set_edit_mode] = useState(true)
	const [btn_edit_text, set_btn_edit_text] = useState("Edit")
	const btn_click = () => {
		set_edit_mode(!edit_mode)
		setEditing(edit_mode)
		if (edit_mode) {
			loadCroppingArea()
			set_btn_edit_text("Save")
		} else {
			saveCropInTask()
			set_btn_edit_text("Edit")
		}
	}
	const setType = (type) => {
		const newTask = task.clone()
		newTask.type = type
		setTask(newTask)
	}
	const setExpected = (expected) => {
		const newTask = task.clone()
		newTask.expectedAnswer = expected
		setTask(newTask)
	}
	const setMaxPoints = (maxPoints) => {
		const newTask = task.clone()
		newTask.maxPoints = maxPoints
		setTask(newTask)
	}
	const setDeductionPerError = (deductionPerError) => {
		const newTask = task.clone()
		newTask.deductionPerError = deductionPerError
		setTask(newTask)
	}
	const onSelectionChange = (event) => {
		const option = options.filter(
			(option) => option.value === event.target.value
		)[0]
		const newTask = task.clone()
		newTask.type = option.value
		setTask(newTask)
	}
	const options = [
		{ value: "text", label: "Text", default: "" },
		{ value: "number", label: "Number", default: "0" },
		{
			value: "text_no_numbers",
			label: "Text without Numbers",
			default: "0",
		},
		{
			value: "single_choice",
			label: "Single Choice Checkbox",
			default: "0",
		},
		//{ value: 'multiple_choice', label: 'Multiple Choice Checkbox', default: '0' },
	]
	return (
		<div
			className={"task"}
			onMouseOver={() => {
				onHover()
			}}
			onMouseLeave={onHoverLeave}
		>
			<div className="buttons" key={"task-buttons" + taskId}>
				<button onClick={() => deleteTask()} disabled={editing}>
					Delete
				</button>
				<button
					onClick={() => btn_click()}
					disabled={editing && edit_mode}
				>
					{btn_edit_text}
				</button>
			</div>

			<div className="form" key={"task-form-div" + taskId}>
				<form className={"taskform"}>
					<div
						className={"type_selector"}
						key={"type_selector" + taskId}
					>
						<label htmlFor="type_selector">Task Type: </label>
						<select
							name="type_selector"
							onChange={onSelectionChange}
							value={task.type}
						>
							{options.map((option) => {
								return (
									<option
										value={option.value}
										key={`${taskId}_${option.value}`}
										onChange={(event) => setType(event.state.value)}
									>
										{option.label}
									</option>
								)
							})}
						</select>
					</div>
					<div className={"max_points"}>
						<label htmlFor="max_points">Max Points:</label>
						<input
							type="number"
							name="max_points"
							min="0"
							value={task.maxPoints}
							onChange={(e) => {
								setMaxPoints(e.target.value)
							}}
						/>
					</div>
					<div className={"deduction_per_error"}>
						<label htmlFor="deduction_per_error">
							Deduction per error:
						</label>
						<input
							type="number"
							name="max_points"
							min="0"
							step="0.5"
							value={task.deductionPerError}
							onChange={(e) => {
								setDeductionPerError(e.target.value)
							}}
						/>
					</div>
					{canEditAnswer && (
						<div
							className={"text_answer"}
							key={"text_answer" + taskId}
						>
							<div>
								<label htmlFor="text_answer">Correct Answer: </label>
								<input
									type="text"
									name="text_answer"
									min="0"
									value={task.expectedAnswer}
									onChange={(e) => {
										setExpected(e.target.value)
									}}
								/>
							</div>
						</div>
					)}
				</form>
			</div>
		</div>
	)
}
export default TaskEditingArea
