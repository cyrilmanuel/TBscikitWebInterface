/**
 * Created by cyriljeanneret on 14.06.17.
 */
class TypeOfButtonList extends React.Component {
    constructor(props) {
        super(props);
        this.typeOfClassifier = this.props.typeOfClassifier;
        this.onClick = this.onClick.bind(this);
    }

    onClick(event) {
        event.target.id
    }

    render() {
        let rows = Object.keys(this.typeOfClassifier).map(name => {
            return (
                <a className="collection-item" onClick={this.onClick} id={name}
                   key={name}>{name}</a>
            );
        });
        return (
            <div className="collection">{rows}</div>
        );
    }
}

window.shareRenderTypeOfButtonList = function (dataClassifier) {
    ReactDOM.render(
        <TypeOfButtonList dataClassifier={dataClassifier}/>,
        document.getElementById('classifier')
    );
};
//---------------------------------------------- BUTTONLIST -------------------------------------
class ButtonList extends React.Component {
    constructor(props) {
        super(props);
        this.dataClassifier = this.props.dataClassifier;
        this.onClick = this.onClick.bind(this);
    }

    onClick(event) {
        window.addShape(event.target.id, this.props.dataClassifier[event.target.id]);
    }

    render() {
        let rows = Object.keys(this.dataClassifier).map(name => {
            return (
                <a className="collection-item" onClick={this.onClick} id={name}
                   key={name}>{name}</a>
            );
        });
        return (
            <div className="collection">{rows}</div>
        );
    }
}
;

window.shareRenderButtonList = function (dataClassifier) {
    ReactDOM.render(
        <ButtonList dataClassifier={dataClassifier}/>,
        document.getElementById('classifier')
    );
};


// ---------------------------------------- list ensemble shape --------------------------------------------

class EnsembleList extends React.Component {
    constructor(props) {
        super(props);
        this.IdEnsembleLearning = this.props.IdEnsembleLearning;
        this.dataClassifier = this.props.dataClassifier;
        this.onClick = this.onClick.bind(this);
        this.onDelete = this.onDelete.bind(this);
    }

    onDelete(event) {
        if (confirm('Are you sure you want to remove the ensemble learning ?')) {
            window.removeShape(this.props.IdEnsembleLearning);
            Materialize.toast('ensemble learning removed !', 2000, 'rounded');
        }
    }

    onClick(event) {
        shareRenderInitFormulaireShape();
        shareRenderFormEnsemble(this.dataClassifier[event.target.id][event.target.name], event.target.name, event.target.id, this.IdEnsembleLearning, this.dataClassifier);
    }

    render() {
        let allrow = "";
        let final = [];
        let rows = [];
        let buttonDelete = <div className="row">
            <div className="col s12">
                <a className="waves-effect waves-light btn" name="Delete" onClick={this.onDelete}
                   key="Delete">Delete Ensemble</a>
            </div>
        </div>;
        for (let idshape in this.dataClassifier) {
            for (let nameClassifier in this.dataClassifier[idshape]) {
                let row = <a className="collection-item" onClick={this.onClick} id={idshape}
                             key={idshape} name={nameClassifier}>{nameClassifier}</a>;
                rows.push(row);
            }
        }
        ;
        allrow = <div className="collection">{rows}</div>
        final.push(buttonDelete);
        final.push(allrow);
        return (
            <div>{final}</div>
        );
    }
}
;

window.shareRenderEnsembleList = function (dataClassifier, IdEnsembleLearning) {
    ReactDOM.render(
        <EnsembleList dataClassifier={dataClassifier} IdEnsembleLearning={IdEnsembleLearning}/>,
        document.getElementById('formClassificator')
    );
};


// ------------------------------------------- Show Form ---------------------------------------

class Formul extends React.Component {
    constructor(props) {
        super(props);
        this.name = this.props.name;
        this.idShape = this.props.idShape;
        this.state = this.props.dict; // trick replace state dict by dict params clasifier
        this.handleDelete = this.handleDelete.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
        window.updateShapeParam(this.idShape, this.state);
    }

    handleDelete(event) {
        if (confirm('Are you sure you want to remove the shape ' + this.name + '?')) {
            window.removeShape(this.idShape);
            Materialize.toast(this.name + ' removed !', 2000, 'rounded');
        }

        event.preventDefault();
    }

    render() {
        return (
            <form key="formParams">
                <div className="row">
                    <div className="col s12">
                        <a className="waves-effect waves-light btn" name="Delete" onClick={this.handleDelete}
                           key="Delete">Delete Shape</a>
                    </div>
                </div>
                {Object.keys(this.state).map(name => {
                    return (
                        <label key={'label' + name}> {name}
                            <input type="text" name={name} value={this.state[name]} onChange={this.handleChange}
                                   placeholder={this.state[name]} key={name}/>
                        </label>
                    );
                })}
            </form>
        );
    }
}
;


window.shareRenderFormShape = function (dictParamsClassifier, nameClassifier, idShape) {
    ReactDOM.render(
        <Formul dict={dictParamsClassifier} name={nameClassifier} idShape={idShape}/>,
        document.getElementById('formClassificator')
    );
};

// -------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------- FORMULAIRE ENSEMBLE ---------------------------------------------
// -------------------------------------------------------------------------------------------------------------------
class FormEnsemble extends React.Component {
    constructor(props) {
        super(props);
        this.name = this.props.name;
        this.state = this.props.dict; // trick replace state dict by dict params clasifier
        this.handleDelete = this.handleDelete.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleList = this.handleList.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
        window.updateShapeEnsembleParam(this.idShape, this.state, this.props.idShapeParent);
    }

    handleDelete(event) {
        if (confirm('Are you sure you want to remove the shape ' + this.name + '?')) {
            window.removeEnsembleShape(this.props.idShapeParent, this.props.idShape);
            Materialize.toast(this.name + ' removed !', 2000, 'rounded');
            //shareRenderInitFormulaireShape();
        }

        event.preventDefault();
    }

    handleList(event) {
        shareRenderInitFormulaireShape();
        shareRenderEnsembleList(this.props.dictAllClassifier, this.props.idShapeParent);
    }

    render() {
        return (
            <form key="formParams">
                <div className="row">
                    <div className="col s6">
                        <a className="waves-effect waves-light btn" name="showList" onClick={this.handleList}
                           key="ShowList">Return</a>
                    </div>
                    <div className="col s6">
                        <a className="waves-effect waves-light btn" name="Delete" onClick={this.handleDelete}
                           key="Delete">Delete Shape</a>
                    </div>
                </div>
                {Object.keys(this.state).map(name => {
                    return (
                        <label key={'label' + name}> {name}
                            <input type="text" name={name} value={this.state[name]} onChange={this.handleChange}
                                   placeholder={this.state[name]} key={name}/>
                        </label>
                    );
                })}
            </form>
        );
    }
}
;

window.shareRenderFormEnsemble = function (dictParamsClassifier, nameClassifier, idShape, idShapeParent, dictAllClassifier) {
    ReactDOM.render(
        <FormEnsemble dict={dictParamsClassifier} name={nameClassifier} idShape={idShape}
                      idShapeParent={idShapeParent} dictAllClassifier={dictAllClassifier}/>,
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
    constructor(props) {
        super(props);
        this.nbRender = this.props.nb;
        this.responseDict = this.props.dict || {};
        this.tabResponseEmpty = Array.apply(null, {length: (this.nbRender - Object.keys(this.responseDict).length)}).map(Number.call, Number)
    }

    render() {
        let result = Object.keys(this.responseDict).map(name => {
                return (
                    <div className="row">
                        <div className="col s12">
                            <div key={name}>Result for {name} {this.responseDict[name]}
                            </div>
                        </div>
                    </div>
                );
            }
        );
        let listItems = Object.keys(this.tabResponseEmpty).map(index => {
                return (
                    <div className="row">
                        <div className="col s12" key={index}>
                            <div className="preloader-wrapper active">
                                <div className="spinner-layer spinner-green-only">
                                    <div className="circle-clipper left">
                                        <div className="circle"></div>
                                    </div>
                                    <div className="gap-patch">
                                        <div className="circle"></div>
                                    </div>
                                    <div className="circle-clipper right">
                                        <div className="circle"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        );
        return (
            <div>{result}{listItems}</div>
        );
    }
}
;

window.shareRenderResult = function (DictResultPost, nbResult) {
    ReactDOM.render(
        <ResultDiv dict={DictResultPost} nb={nbResult}/>,
        document.getElementById('response')
    );
};
window.shareRenderResetResult = function () {
    ReactDOM.render(
        <div></div>,
        document.getElementById('response')
    );
};