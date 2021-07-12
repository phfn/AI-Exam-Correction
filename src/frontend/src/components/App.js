import TaskSelector from './TaskSelector';
import ReviewOverview from './ReviewOverview';
import Header from './Header';
import Footer from './Footer';
import {useState} from "react";
import sampleExamContainer from '../SampleDocument';
import {ExamContainer, Exam} from "./ExamContainer";
import ReviewExam from "./ReviewExam/ReviewExam";

const App = () => {
	const [examContainer, setExamContainer] = useState(
		process.env.REACT_APP_TEST === "overview"
		? sampleExamContainer
		: new ExamContainer(new Exam()))
	const [state, setState] = useState(
		process.env.REACT_APP_TEST === "overview" ? 1 : 0
	)
	const [selectedExam, setSelectedExam] = useState()
	return(
		<div className="Site">
			<Header title="Automatic Exam Correction" />
			<div className="App">
				{state === 0 &&
					<TaskSelector
						exam = {examContainer.correctExam}
						setExam={(exam) => {
							let n = examContainer.clone();
							n.correctExam = exam;
							setExamContainer(n)
						}}
						examContainer={examContainer}
                        setExamContainer={setExamContainer}
						setStudentExams={(examImages, filenames) => {
							let n = examContainer.clone();
							n.studentExams = examImages.map((image, index) => {
								return new Exam(image, filenames[index], examContainer.correctExam.tasks)
							});
							setExamContainer(n);
						}}
						leave={ () => setState(state+1) }
					/>
				}
				{state === 1 && <ReviewOverview
					examContainer={examContainer}
					reviewExam={(exam) => {setSelectedExam(exam); setState(state+1)}}
				/>}
				{state === 2 && <div>Hallo {selectedExam.filename}</div>}
				{state > 2 && <ReviewExam selectedExam={selectedExam}/>}
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
