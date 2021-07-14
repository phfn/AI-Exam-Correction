import TaskReviewingArea from "./TaskReviewingArea"
const TaskReviewingAreas = ({tasks, setTasks, hover}) => {

	let setTask = (index, newTask) => {
	    let n = tasks.map((task)=>{return task.clone()})
        n[index] = newTask.clone()
        setTasks(n)
	}

    return(
        <div className="Tasks">
        {tasks.map(
                (task, index) =>
                    <TaskReviewingArea
                        key={index}
                        task={task}
                        taskId={index}
                        setTask={(newTask) => {setTask(index, newTask)}}
						hover={hover}
                    />
            )}
        </div>
    )
}
export default TaskReviewingAreas
