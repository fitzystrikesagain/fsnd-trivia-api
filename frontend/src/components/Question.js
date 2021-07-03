import React, {Component} from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
    constructor() {
        super();
        this.state = {
            visibleAnswer: false
        }
    }

    flipVisibility() {
        this.setState({visibleAnswer: !this.state.visibleAnswer});
    }

    render() {
        let {question, answer, category, difficulty} = this.props;

        // the array index begins at zero
        // this is a hacky solution to offset the category svgs
        const svgOffsetMap = {
            "Art": "science.svg",
            "Science": "geography.svg",
            "Geography": "art.svg",
            "History": "geography.svg",
            "Entertainment": "history.svg",
            "Sports": "entertainment.svg",
            undefined: "sports.svg"
        }

        return (
            <div className="Question-holder">
                <div className="Question">{question}</div>
                <div className="Question-status">
                    <img className="category"
                         alt="category icon svg"
                         src={`../../${svgOffsetMap[category]}`}/>
                    <div className="difficulty">Difficulty: {difficulty}</div>
                    <img alt="rubbish bin" src="../../delete.png"
                         className="delete"
                         onClick={() => this.props.questionAction('DELETE')}/>

                </div>
                <div className="show-answer button"
                     onClick={() => this.flipVisibility()}>
                    {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
                </div>
                <div className="answer-holder">
                    <span
                        style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
                </div>
            </div>
        );
    }
}

export default Question;
