import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import TaskSelector from './components/TaskSelector';
import Header from './components/Header';
import Footer from './components/Footer';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
	<React.StrictMode>
		<div className="Site">
			<Header title="Automatic Exam Correction" />
			<div className="App">
				<TaskSelector />
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
	</React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
