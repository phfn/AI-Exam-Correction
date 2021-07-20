import React from 'react'
const Footer = ({ links }) => {
	return(
		<div className="footer">
			{links.map( ({href, title}, index) => { return(
				<a
					href={href}
					key={"fl"+index}>
					{title}
				</a>)
			} )}
		</div>
	)
}

export default Footer
