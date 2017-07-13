/**
 * Created by cyriljeanneret on 14.06.17.
 */
class TypeOfButtonList extends React.Component {
    constructor(props) {
        super(props);
        this.dataClassifier = this.props.dataClassifier;
        this.typeOfClassifier = this.props.typeOfClassifier;
        this.onClick = this.onClick.bind(this);
    }

    onClick(event) {
        window.shareRenderButtonList(this.dataClassifier, event.target.name);
    }

    render() {
        let rows = Object.keys(this.dataClassifier).map(name => {
            return (
                <a className="collection-item" onClick={this.onClick} name={name}
                   key={name}>{name}</a>
            );
        });
        return (
        <div className="row">
            <div className="collection">{rows}</div>
            </div>
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
        this.allDataClassifier = this.props.allDataClassifier;
        this.typeOfDataClassifier= this.props.typeOfDataClassifier;
        this.descriptionDataClassifier =this.allDataClassifier[this.typeOfDataClassifier][1];
        this.dataClassifier = this.allDataClassifier[this.typeOfDataClassifier][0];
        this.onClick = this.onClick.bind(this);
        this.handleReturn = this.handleReturn.bind(this);
    }

    handleReturn(event){
      shareRenderResetButtonList();
      shareRenderTypeOfButtonList(this.allDataClassifier);
    }

    onClick(event) {
        window.addShape(event.target.id, this.dataClassifier[event.target.id], this.descriptionDataClassifier[event.target.id],this.typeOfDataClassifier);
    }

    render() {
        let rows = Object.keys(this.dataClassifier).map(name => {
            return (
                <a className="collection-item" onClick={this.onClick} id={name}
                   key={name}>{name}</a>
            );
        });
        return (
            <div className="row">
                <a className="waves-effect waves-light btn" name="return" onClick={this.handleReturn}
                   key="return">Return</a>
            <div className="collection">{rows}</div>
            </div>
        );
    }
}
;

window.shareRenderButtonList = function (allDataClassifier, typeOfDataClassifier) {
    ReactDOM.render(
        <ButtonList allDataClassifier={allDataClassifier} typeOfDataClassifier={typeOfDataClassifier}/>,
        document.getElementById('classifier')
    );
};

window.shareRenderResetButtonList = function () {
    ReactDOM.render(
        <div></div>,
        document.getElementById('classifier')
    );
};


// ---------------------------------------- list ensemble shape --------------------------------------------

class EnsembleList extends React.Component {
    constructor(props) {
        super(props);
        this.IdEnsembleLearning = this.props.IdEnsembleLearning;
        this.dataClassifier = this.props.dataClassifier;
        this.descriptionClassifier = this.props.descriptionClassifier;
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
        shareRenderFormEnsemble(this.dataClassifier[event.target.id][event.target.name],this.descriptionClassifier[event.target.id][event.target.name], event.target.name, event.target.id, this.IdEnsembleLearning, this.dataClassifier, this.descriptionClassifier);
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

window.shareRenderEnsembleList = function (dataClassifier,descriptionClassifier, IdEnsembleLearning) {
    ReactDOM.render(
        <EnsembleList dataClassifier={dataClassifier} IdEnsembleLearning={IdEnsembleLearning} descriptionClassifier={descriptionClassifier}/>,
        document.getElementById('formClassificator')
    );
};


// ------------------------------------------- Show Form ---------------------------------------

class Formul extends React.Component {
    constructor(props) {
        super(props);
        this.name = this.props.name;
        this.dictDescriptionParamsClassifier = this.props.dictDescriptionParamsClassifier;
        this.idShape = this.props.idShape;
        this.state = this.props.dict; // trick replace state dict by dict params clasifier
        this.handleDelete = this.handleDelete.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleInfo = this.handleInfo.bind(this);
        this.handleDownload = this.handleDownload.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value},()=>window.updateShapeParam(this.idShape, this.state));
    }

    handleInfo(event) {
        alert(this.dictDescriptionParamsClassifier[event.currentTarget.name]);
    }

    handleDownload(event){
        window.startDownload(this.idShape);
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
                    <div className="col s6">
                        <a className="waves-effect waves-light btn" name="Delete" onClick={this.handleDelete}
                           key="Delete">Delete Shape</a>
                    </div>
                    <div className="col s6">
                        <a className="waves-effect waves-light btn" name="DL" onClick={this.handleDownload}
                           key="download">DL Model</a>
                    </div>
                </div>
                <div className="row">
                    ID of the shape : {this.props.idShape}
                </div>
                {Object.keys(this.state).map(name => {
                    return (
                        <div key={'row-' + name} className="row">
                            <div className="col s6">
                                <label key={'label-' + name}> {name}</label>
                            </div>
                            <div className="col s6">
                                <a className="btn-flat-tiny waves-effect waves-light" name={name}
                                   onClick={this.handleInfo} key={'btn-' + name}><i className="material-icons">info_outline</i></a>
                            </div>
                            <div className="col s12">
                                <input type="text" name={name} value={this.state[name]} id={name}
                                       onChange={this.handleChange}
                                       placeholder={this.state[name]} key={name}/>
                            </div>
                        </div>
                    );
                })}
            </form>
        );
    }
}


window.shareRenderFormShape = function (dictParamsClassifier, dictDescriptionParamsClassifier, nameClassifier, idShape) {
    ReactDOM.render(
        <Formul dict={dictParamsClassifier} name={nameClassifier} idShape={idShape}
                dictDescriptionParamsClassifier={dictDescriptionParamsClassifier}/>,
        document.getElementById('formClassificator')
    );
};

// -------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------- FORMULAIRE ENSEMBLE ---------------------------------------------
// -------------------------------------------------------------------------------------------------------------------
class FormEnsemble extends React.Component {
    constructor(props) {
        super(props);
        this.idShape = this.props.idShape;
        this.name = this.props.name;
        this.state = this.props.dict; // trick replace state dict by dict params clasifier
        this.allClassifier = this.props.dictAllClassifier;
        this.handleDelete = this.handleDelete.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleList = this.handleList.bind(this);
        this.handleInfo = this.handleInfo.bind(this);
    }

    handleInfo(event){
        alert(this.props.dictDescriptionParamsClassifier[event.currentTarget.name]);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value},function(){
            window.updateShapeEnsembleParam(this.idShape, this.state, this.props.idShapeParent, this.name);
            this.allClassifier[this.idShape][this.name] = this.state;
        });
    }

    handleDelete(event) {
        if (confirm('Are you sure you want to remove the shape ' + this.name + '?')) {
            window.removeEnsembleShape(this.props.idShapeParent, this.props.idShape);
            Materialize.toast(this.name + ' removed !', 2000, 'rounded');
        }

        event.preventDefault();
    }

    handleList(event) {
        shareRenderInitFormulaireShape();
        shareRenderEnsembleList(this.props.dictAllClassifier, this.props.dictAllDescription, this.props.idShapeParent);
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
                <div className="row">
                    ID of the shape : {this.props.idShape}
                </div>
                {Object.keys(this.state).map(name => {
                   return (
                        <div key={'row-' + name} className="row">
                            <div className="col s6">
                                <label key={'label-' + name}> {name}</label>
                            </div>
                            <div className="col s6">
                                <a className="btn-flat-tiny waves-effect waves-light" name={name}
                                   onClick={this.handleInfo} key={'btn-' + name}><i className="material-icons">info_outline</i></a>
                            </div>
                            <div className="col s12">
                                <input type="text" name={name} value={this.state[name]} id={name}
                                       onChange={this.handleChange}
                                       placeholder={this.state[name]} key={name}/>
                            </div>
                        </div>
                    );
                })}
            </form>
        );
    }
}
;

window.shareRenderFormEnsemble = function (dictParamsClassifier,dictDescriptionParamsClassifier, nameClassifier, idShape, idShapeParent, dictAllClassifier,dictAllDescription) {
    ReactDOM.render(
        <FormEnsemble dict={dictParamsClassifier} name={nameClassifier} idShape={idShape}
                      idShapeParent={idShapeParent} dictAllClassifier={dictAllClassifier}
                       dictDescriptionParamsClassifier={dictDescriptionParamsClassifier} dictAllDescription={dictAllDescription} />,
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
        this.tabResponseEmpty = Array.apply(null, {length: (this.nbRender - Object.keys(this.responseDict).length)}).map(Number.call, Number);
        this.handleShowMatrix = this.handleShowMatrix.bind(this);
    }

    handleShowMatrix(event) {

        let data = {};
        data[Object.keys(this.responseDict[event.target.name])[0]] = this.responseDict[Object.keys(this.responseDict[event.target.name])[0]];
        axios.post('/index/matrix', {
            params: data,
        })
            .then(function (response) {
                window.renderMatrix(response);
            })
            .catch(function (error) {
                console.log(error);
            });

    }

    render() {
        let result = Object.keys(this.responseDict).map(name => {
                return (
                    <div className="row" key={"row-"+name}>
                        <div className="col s10" key={"cols10-"+name}>
                            <div key={name}>Result for {Object.keys(this.responseDict[name])[0]} {this.responseDict[name][Object.keys(this.responseDict[name])[0]]['resultat']}
                            </div>
                        </div>
                        <div className="col s2" key={"cols2-"+name}>
                            <a className="waves-effect waves-light btn-small" name={name} onClick={this.handleShowMatrix}
                               key={"btnMatrix" + name}>Show Matrix</a>
                        </div>
                    </div>
                );
            }
        );
        let listItems = Object.keys(this.tabResponseEmpty).map(index => {
                return (
                    <div className="row" key={"rowr-"+index}>
                        <div className="col s12" key={index}>
                            <div className="preloader-wrapper active"  key={"preload-"+index}>
                                <div className="spinner-layer spinner-green-only"  key={"spinner-"+index}>
                                    <div className="circle-clipper left"  key={"circle-"+index}>
                                        <div className="circle"  key={"cir-"+index}></div>
                                    </div>
                                    <div className="gap-patch"  key={"gap-"+index}>
                                        <div className="circle"  key={"circl-"+index}></div>
                                    </div>
                                    <div className="circle-clipper right" key={"clipper-"+index}>
                                        <div className="circle"  key={"lastcircle-"+index}></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        );
        return (
            <div  key="Result">{result}{listItems}</div>
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