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
                    <button className="btn waves-effect waves-light" onClick={this.onClick} id={item}
                            key={item}>{item}</button>
                );
            }
        );

        return (
            <div className="col s12">{rows}</div>
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