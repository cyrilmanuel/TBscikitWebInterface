/**
 * Created by cyriljeanneret on 14.06.17.
 */
class ButtonList extends React.Component {
    onClick(event) {
        clictodraw(event.target.id);
    }

    render() {
        let items = this.props.items || []
        let rows = items.map(
            item => {
                return (
                    <li className="collection-item" onClick={this.onClick} id={item}
                        key={item}>{item}</li>
                );
            }
        );
        return (
            <ul className="collection">{rows}</ul>
        );
    }
}

window.shareRenderButtonList = function (tab) {
    ReactDOM.render(
        <ButtonList items={tab}/>,
        document.getElementById('app')
    );
};

// ------------------------------------------- Show Form ---------------------------------------

class FormShape extends React.Component {
    render() {
        let dict = this.props.dict || {}
        let valueParams = this.props.valueParam || []
        let items = this.props.nameParam || []

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

window.shareRenderFormShape = function (dictParamsClassifier) {

    var nameParams = [];
    var valueParams = [];
    for (var key in dictParamsClassifier) {
        nameParams.push(key);
        valueParams.push(dictParamsClassifier[key]);
    }

    ReactDOM.render(
        <FormShape nameParam={nameParams} valueParam={valueParams} dict={dictParamsClassifier}/>,
        document.getElementById('formClassificator')
    );
};
