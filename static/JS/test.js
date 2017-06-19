/**
 * Created by cyriljeanneret on 14.06.17.
 */
class Greeting extends React.Component {
    render() {
        return <h1>Hello</h1>;
    }

    unmount() {
        ReactDOM.unmountComponentAtNode();
    }
}

window.shareRenderFunc = function () {
    ReactDOM.render(<Greeting />, document.getElementById('app'));
};
window.shareRenderFunc2 = function () {
    ReactDOM.render(<div></div>, document.getElementById('app'));
};
