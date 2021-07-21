import React from "react"
import TaskReviewingArea from "./TaskReviewingArea"
const TaskReviewingAreas = ({ tasks, setTasks, setHoverIndex }) => {
	const setTask = (index, newTask) => {
		const newTasks = tasks.map((task) => {
			return task.clone()
		})
		newTasks[index] = newTask.clone()
		setTasks(newTasks)
	}

	return (
		<div className="Tasks">
			{tasks.map((task, index) => (
				<TaskReviewingArea
					key={index}
					task={task}
					taskId={index}
					setTask={(newTask) => {
						setTask(index, newTask)
					}}
					hover={() => {
						setHoverIndex(index)
					}}
					onHoverLeave={() => {
						setHoverIndex(-1)
					}}
				/>
			))}
		</div>
	)
}
export default TaskReviewingAreas
