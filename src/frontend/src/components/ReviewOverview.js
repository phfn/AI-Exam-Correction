import './ReviewOverview.css'
function ReviewOverview({examContainer, reviewExam}){
    const formatPoints = (number, max_length) => {
        let str = number.toString()
        let len = max_length - str.length
        str = len > 0 ?  " ".repeat(len) + str : str
        return str
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
								<td><button onClick={() => {reviewExam(exam)}}>Review</button></td>
                                </tr>
                        })}

                    </tbody>
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
