function Rectangle({className, id, x=0, y=0, height=100, width=300}){
	return(
		<div className={"canvas rectangle " + className} id={id} style={{left:x, top:y, height:height, width:width}}/>
	)
}
export default Rectangle
