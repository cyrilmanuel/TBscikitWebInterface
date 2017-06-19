/**
 * Created by cyriljeanneret on 13.06.17.
 */


// {"Clf":"SVM","GridSearch":1, "ParamsGrid":[{"C": [1, 10, 100, 1000], "kernel": ["rbf"]}],"Result":"None"}

class DataToJson {
    constructor() {
        this._Clf = "";
        this._ParamsClf = {};
        this._GridSearch = 1;
        this._ParamsGrid = [{"C": [1, 10, 100, 1000], "kernel": ["rbf"]}];
        this._Result = "None";
    }

    get Clf() {
        return this._Clf;
    }

    set Clf(value) {
        this._Clf = value;
    }

    get ParamsClf() {
        return this._ParamsClf;
    }

    set ParamsClf(value) {
        this._ParamsClf = value;
    }

    get GridSearch() {
        return this._GridSearch;
    }

    set GridSearch(value) {
        this._GridSearch = value;
    }

    get ParamsGrid() {
        return this._ParamsGrid;
    }

    set ParamsGrid(value) {
        this._ParamsGrid = value;
    }

    get Result() {
        return this._Result;
    }

    set Result(value) {
        this._Result = value;
    }

    getJsonifyData() {
        var DataRequest = JSON.stringify(
            {
                "Clf": this._Clf,
                "ParamsClf": this._ParamsClf,
                "GridSearch": this._GridSearch,
                "ParamsGrid": this._ParamsGrid,
                "Result": this._Result
            });
        return DataRequest;
    }

    setResponseToObject(JsonData){
        var temp = JSON.parse(JsonData);
        console.log(temp);
    }
}