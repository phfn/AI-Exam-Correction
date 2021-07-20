import React from 'react'
const Header = ({ title }) => {
	return(
		<div className="header">
			<p className="title">
				{title}
			</p>
		</div>
	)
}
Header.defaultProps = {
	title: "Frontend"
}

export default Header
