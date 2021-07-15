import './ReviewOverview.css'
import {useState} from "react"
function ReviewOverview({examContainer, reviewExam}){
	let userLang = navigator.language || navigator.userLanguage; 
	let isGerman = userLang.toUpperCase() === "de-DE".toUpperCase() || userLang.toUpperCase() === "DE"
	const [delimiter, setDelimiter] = useState(
		//exels parses diffrent in diffrent language settings
		isGerman ? ';' : ',' 
	)
    const formatPoints = (number, max_length) => {
        let str = number.toString()
        let len = max_length - str.length
        str = len > 0 ?  " ".repeat(len) + str : str
        return str
    }
	const downloadFile = (blob, fileName) => {
	  const link = document.createElement('a');
	  // create a blobURI pointing to our Blob
	  link.href = URL.createObjectURL(blob);
	  link.download = fileName;
	  // some browser needs the anchor to be in the doc
	  document.body.append(link);
	  link.click();
	  link.remove();
	  // in case the Blob uses a lot of memory
	  setTimeout(() => URL.revokeObjectURL(link.href), 7000);
	};

	const downloadCsv = () => {

		let csv = examContainer.studentExams.reduce((str, exam) => {

			// Sum up
			let max_points = exam.tasks.reduce((sum, task) => { return sum + task.maxPoints }, 0)
			let points = exam.tasks.reduce((sum, task) => { return sum + task.points }, 0)

			let percentage = Math.round(points/max_points*100)
			return `${str}\n${exam.filename}${delimiter}${points}${delimiter}${max_points}${delimiter}${percentage}%`

		}, `Document${delimiter}Points${delimiter}Max${delimiter}Percentage`)

		let b = new Blob([csv], {type: 'text/csv'})
		downloadFile(b, "results.csv")
	}
	return(
        <div className="ReviewOverview">
            <div className="column column-left">
                <h1>Exams</h1>
                <div className="tableFixedHead">
                <table>
                    <thead>
                    <tr>
                        <th>Document</th>
                        <th>Result</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                        {examContainer.studentExams.map((exam, index) => {
                            let max = exam.tasks.reduce((sum, task ) => {
                                return sum + task.maxPoints
                            }, 0)
                            let points = exam.tasks.reduce((sum, task) => {
                                return sum + task.points
                            }, 0)
                            return <tr key={`${exam} ${index}`}>
                                <td>{exam.filename}</td>
                                <td>
                                    <div className="points">
                                        {points}/{max}
                                    </div>
                                </td>
								<td><button onClick={() => {reviewExam(index)}}>Review</button></td>
                                </tr>
                        })}

                    </tbody>
					<tfoot>
						<tr>
							<td> Delimiter: </td>
							<td>
								<select
									name="type_selector"
									value={delimiter}
									onChange={(event) => {setDelimiter(event.target.value)}}
								>
									{[",",";"].map( (option) => {
										return(
											<option
												value={option}
												key={"option-" + option}
											>
												{option}
											</option>
										)
									})}
								</select>
							</td>
							<td>
								<button onClick={downloadCsv}>Download .csv</button>
							</td>
						</tr>
					</tfoot>

                </table>
                </div>
            </div>
            <div className="column column-right">
                <h1>Tasks</h1>
                <div className="tableFixedHead">
                <table>
                    <thead>
                    <tr>
                        <th>№</th>
                        <th>Type</th>
                        <th>ØResult</th>
                    </tr>
                    </thead>
                    <tbody>
                        {examContainer.correctExam.tasks.map((task, index) => {
                            let points = examContainer.studentExams.reduce((sum, exam) => {
                                return sum + exam.tasks[index].points
                            }, 0)
                            let len = examContainer.studentExams.length
                            return <tr key={`exams_tasks ${index}`}>
                                <td>{index+1}</td>
                                <td>
                                    {task.type}
                                </td>
                                <td>
                                    <div className="points">
                                        {(points/len).toFixed(1)}/{formatPoints(task.maxPoints, 2)}
                                    </div>
                                </td>
                                </tr>
                        })}

                    </tbody>
                </table>
                </div>
            </div>
        </div>
	)
}
export default ReviewOverview
