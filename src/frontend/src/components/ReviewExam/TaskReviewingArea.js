import React from "react"
const TaskReviewingArea = ({
	task,
	setTask,
	taskId,
	hover,
	onHoverLeave,
}) => {
	const setPoints = (points) => {
		const newTask = task.clone()
		newTask.points = points
		setTask(newTask)
	}

	return (
		<div
			className={"task"}
			onMouseLeave={onHoverLeave}
			onMouseOver={() => {
				hover(taskId)
			}}
		>
			<div className="form" key={"task-form-div" + taskId}>
				<div className="answers">
					<table>
						<thead>
							<td>Correct:</td>
							<td>Student:</td>
						</thead>
						<tbody>
							<tr>
								<td className="answer">{task.expectedAnswer}</td>
								<td className="answer">{task.actualAnswer}</td>
							</tr>
						</tbody>
					</table>
				</div>
				<input
					type="number"
					value={task.points}
					size="2"
					onChange={(e) => {
						setPoints(parseFloat(e.target.value))
					}}
				/>
				/{task.maxPoints}
			</div>
		</div>
	)
}
export default TaskReviewingArea
