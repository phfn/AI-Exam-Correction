
class ExamContainer{
	constructor(correctExam, studentExams = []){
		this.correctExam = correctExam
		this.studentExams = studentExams
	}
	clone(){
		return new ExamContainer(this.correctExam, this.studentExams.map((exam) => {return exam.clone()}))
	}
	static fromJSON(json){
	    return new ExamContainer(
	        Exam.fromJSON(json.correctExam),
			json.studentExams.map((exam) =>{
				return Exam.fromJSON(exam)
			})
		)
	}
}
class Exam{
	constructor(image = "", filename="", tasks = [], imageModified=null){
		this.image = image
        this.filename = filename
		this.tasks = tasks
		this.imageModified = imageModified == null ? image : imageModified
	}
	clone(){
	    return new Exam(this.image, this.filename, this.tasks, this.imageModified)
	}
	static fromJSON(json){
		return new Exam(
			json.image,
			json.filename,
			json.tasks.map((task) =>{
				return Task.fromJSON(task)
			}),
			json.imageModified
			)
	}
}
class Task{
	constructor(x,y,width,height,type="text",expectedAnswer="", maxPoints=10, deductionPerError=1, actualAnswer="", points=0){
		this.x = x
		this.y = y
		this.width = width
		this.height = height
		this.type = type
		this.expectedAnswer = expectedAnswer
		this.maxPoints = maxPoints
		this.deductionPerError = deductionPerError
		this.actualAnswer = actualAnswer
		this.points = points
	}
	clone(){
		return new Task(this.x, this.y, this.width, this.height, this.type, this.expectedAnswer, this.maxPoints, this.deductionPerError, this.actualAnswer, this.points)
	}
	static fromJSON(json){
		return new Task(
			json.x,
			json.y,
			json.width,
			json.height,
			json.type,
			json.expectedAnswer,
			json.maxPoints,
			json.deductionPerError,
			json.actualAnswer,
			json.points
		)
	}
}

export {ExamContainer, Exam, Task}
