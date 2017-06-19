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

window
    .shareRenderFunc5 = function (tab) {
    ReactDOM.render(
        <ButtonList items={tab}/>,
        document.getElementById('app')
    );
};