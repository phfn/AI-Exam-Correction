import exameImg from "./pics/exame.jpg"
import { ExamContainer, Exam, Task } from "./components/ExamContainer"

const generateTasks = () => {
	const tasks = []
	for (let i = 0; i < 43; i++) {
		const max_points = parseInt(Math.random() * 10 + 5)
		const points = parseInt(Math.random() * max_points)

		tasks.push(
			new Task(
				Math.random() * 700,
				Math.random() * 5000,
				Math.random() * 500,
				Math.random() * 500,
				"text",
				"wahr",
				max_points,
				1,
				"falsch",
				points
			)
		)
	}
	return tasks
}

const exams__ = []
for (let i = 0; i < 43; i++) {
	exams__.push(new Exam(exameImg, "HECTOR.pdf", generateTasks()))
}
const examContainer = new ExamContainer(
	new Exam("", "", generateTasks(), ""),
	exams__
)
export default examContainer
