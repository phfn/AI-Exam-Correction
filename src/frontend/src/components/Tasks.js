import Task from "./Task"
const Tasks = ({tasks, setTasks, load, del, save, editing, setEditing, canEditAwnser}) => {

	let setTask = (task_to_edit) => {
        let newTasks = tasks.map((task) => {
                if (task.id === task_to_edit.id) {
					return task_to_edit
                } else {
					return task
                }
            }
        )
		setTasks(newTasks)
	}

		

    return(
        <div className="Tasks">
        {tasks.map(
                (task) =>  <Task key={task.id} task={task} setTask={setTask} load={load} del={del} editing={editing} save={save} setEditing={setEditing} canEditAwnser={canEditAwnser}/>
            )}
        </div>
    )
}
export default Tasks
