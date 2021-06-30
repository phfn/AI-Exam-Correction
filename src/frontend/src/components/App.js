import TaskSelector from './TaskSelector';
import Header from './Header';
import Footer from './Footer';
import {useState} from "react";
import exame from '../pics/exame.jpg'

const App = () => {
	const [document, setDocument] = useState({
		taskList: {tasks:[], i: 0},
		image: exame,
		exams: []
	})
	const [state, setState] = useState(0)
	return(
		<div className="Site">
			<Header title="Automatic Exam Correction" />
			<div className="App">
				{state === 0 && <TaskSelector canEditAwnser={false} document={document} setDocument={setDocument} leave={ () => setState(state+1) }/>}
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
