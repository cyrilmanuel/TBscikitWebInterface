/**
 * Created by cyriljeanneret on 14.06.17.
*/

class ButtonList extends React.Component {
    onClick(event) {
        window.addShape(event.target.id);
    }
    render() {
        let items = this.props.items || []
        let rows = items.map(
            item => {
                return (
                    <a className="collection-item" onClick={this.onClick} id={item}
                        key={item}>{item}</a>
                );
            }
        );
        return (
            <div className="collection">{rows}</div>
        );
    }
};

window.shareRenderButtonList = function (tab) {
    ReactDOM.render(
        <ButtonList items={tab}/>,
        document.getElementById('classifier')
    );
};

// ------------------------------------------- Show Form ---------------------------------------

// class FormShape extends React.Component {
//     render() {
//         let dict = this.props.dict || {}
//         let label = Object.keys(dict).map(name => {
//                     return (
//                         <div>{name} : {dict[name]}</div>
//                     );
//             }
//         );
//         return (
//             <div>{label}</div>
//         );
//     }
// };


//------------------------------------- LabelForm ---------------------------------------
class Formul extends React.Component {
    constructor(props) {
        super(props);
        // TODO CHANGE NULL VALUE BY " "
        this.state = this.props.dict;
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name] : event.target.value});
    }

    handleSubmit(event) {
        // TODO CALL FUNCTION INTO THE SHAPE TO REPLACE DICT SHAPE BY THIS STATE DICT
        alert('A name was submitted: ' + this.state['C']);
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                {Object.keys(this.props.dict).map(name => {
                return (
                    <label> {name}
                    <input type="text" name={name} value={this.state[name]} onChange={this.handleChange} placeholder={name}/>
                    </label>
                );
            })}
                <input type="submit" value="Submit"/>
            </form>
        );
    }
};


window.shareRenderFormShape = function (dictParamsClassifier) {
    ReactDOM.render(
        <Formul dict={dictParamsClassifier}/>,
        document.getElementById('formClassificator')
    );
};

window.shareRenderInitFormulaireShape = function () {
    ReactDOM.render(
        <div></div>,
        document.getElementById('formClassificator')
    );
};
// ------------------------ RENDER RETURN RESULT OF JSON -----------------------

class ResultDiv extends React.Component {
    render() {
        let dict = this.props.dict || {}
        let result = Object.keys(dict).map(name => {
                return (
                    <div>id of the shape = {name}  {dict[name]}
                    </div>
                );
            }
        );
        return (
            <div>{result}</div>
        );
    }
};

window.shareRenderResult = function (DictResultPost) {

    ReactDOM.render(
        <ResultDiv dict={DictResultPost}/>,
        document.getElementById('response')
    );
};