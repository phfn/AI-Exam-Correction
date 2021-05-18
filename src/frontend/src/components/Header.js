const Header = ({ title }) => {
    return(
        <header>
            <h1 style={{color: "red", backgroundColor:"green"}}>
                {title}
            </h1>
        </header>
    )
}
Header.defaultProps = {
    title: "Frontend"
}

export default Header
