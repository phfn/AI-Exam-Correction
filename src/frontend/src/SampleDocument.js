import exameImg from './pics/exame.jpg'
import {Exam, Task} from "./components/ExamContainer";


const generateTasks = () => {
	let tasks = []
	for (let i = 0; i < 43; i++){
		let max_points = parseInt(Math.random()*10+5)
		let points = parseInt(Math.random()*max_points)

		tasks.push(new Task( 0, 0, 20, 30, "text", "wahr", max_points, 1, "falsch", points ))
	}
	return tasks
}

let exams__ = []
for (let i = 0; i < 43; i++){
	exams__.push(
		new Exam("", 'HECTOR.pdf', generateTasks())
	)
}
let examContainer =
    {
        correctExam: new Exam("", '', generateTasks(), ""),
		studentExams: exams__
    }
export default examContainer
