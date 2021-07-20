import TaskSelector from './TaskSelector'
import ReviewOverview from './ReviewOverview'
import Header from './Header'
import Footer from './Footer'
import {React, useState} from "react"
import sampleExamContainer from '../SampleDocument'
import {ExamContainer, Exam} from "./ExamContainer"
import ReviewExam from "./ReviewExam/ReviewExam"

const App = () => {
	const [examContainer, setExamContainer] = useState(
		process.env.REACT_APP_TEST === "overview"
			? sampleExamContainer
			: new ExamContainer(new Exam()))
	const [state, setState] = useState(
		process.env.REACT_APP_TEST === "overview" ? 1 : 0
	)
	const [selectedExamIndex, setSelectedExamIndex] = useState()
	const setExam = (index, newExam) =>{
		let n = examContainer.clone()
		n.studentExams[index] = newExam
		setExamContainer(n)
	}
	return(
		<div className="Site">
			<Header title="Automatic Exam Correction" />
			<div className="App">
				{state === 0 &&
					<TaskSelector
						exam = {examContainer.correctExam}
						setExam={(exam) => {
							let n = examContainer.clone()
							n.correctExam = exam
							setExamContainer(n)
						}}
						examContainer={examContainer}
						setExamContainer={setExamContainer}
						setStudentExams={(examImages, filenames) => {
							let n = examContainer.clone()
							n.studentExams = examImages.map((image, index) => {
								return new Exam(image, filenames[index], examContainer.correctExam.tasks)
							})
							setExamContainer(n)
						}}
						leave={ () => setState(state+1) }
					/>
				}
				{state === 1 && <ReviewOverview
					examContainer={examContainer}
					reviewExam={(examIndex) => {setSelectedExamIndex(examIndex); setState(state+1)}}
				/>}
				{state === 2 && <ReviewExam exam={examContainer.studentExams[selectedExamIndex]} setExam={(newExam) => {setExam(selectedExamIndex, newExam)}} goBack={() => {setState(state-1)}}/>}
				{state > 2 && <div>404</div>}
			</div>
			<Footer links={[
				{
					title: "Source",
					href: "https://git.thm.de/tnhm62/swtp-1-ki-ocr"
				},
				{
					title: "THM",
					href: "https://thm.de"
				},
				{
					title: "Impressum",
					href: "/impressum"
				}
			]} />
		</div>
	)
}
export default App
