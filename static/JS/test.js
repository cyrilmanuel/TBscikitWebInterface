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
}

window.shareRenderButtonList = function (tab) {
    ReactDOM.render(
        <ButtonList items={tab}/>,
        document.getElementById('classifier')
    );
};

// ------------------------------------------- Show Form ---------------------------------------

class FormShape extends React.Component {
    render() {
        let dict = this.props.dict || {}
        let label = Object.keys(dict).map(name => {
                if (dict[name] == true) {
                    return (
                        <div>{name} : true</div>
                    );
                } else {
                    return (
                        <div>{name} : {dict[name]}</div>
                    );
                }
            }
        );
        return (
            <div>{label}</div>
        );
    }
}
;


//------------------------------------- LabelForm ---------------------------------------
class LabelForForm extends React.Component {
    render() {
        return (
            <div>
                <label for={this.props.forLabel}>{this.props.nameLabel}</label>
                {this.props.children}
            </div>
        );
    }
}
;


class inputForForm extends React.Component {
    render() {
        let t = this.props.t;
        return (
            <LabelForForm nameLabel={"hello"}>
                <div> parent</div>
            </LabelForForm>
        );
    };
}


window.shareRenderFormShape = function (dictParamsClassifier) {
    ReactDOM.render(
        <FormShape dict={dictParamsClassifier}/>,
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
}

window.shareRenderResult = function (DictResultPost) {

    ReactDOM.render(
        <ResultDiv dict={DictResultPost}/>,
        document.getElementById('response')
    );
};