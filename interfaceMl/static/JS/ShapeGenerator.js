(function () {

    // constructor shape
    function ShapeGenerator(nameOfficeID, nameClassifier, dictParamsClassifier, dictDescriptionParamsClassifier, sizeCanvas, typeOfClassifier) {
        this.Container_constructor();
        // stock the name of the classifier this shape will be repr
        this.name = nameOfficeID.toString();

        this.typeOfClassifier = typeOfClassifier;
        // stock the params of the classifier into the shape
        // because this shape can call the function to render
        // with React, a approprieted form
        this.dicParamsClassifier = dictParamsClassifier;
        this.dictDescriptionParamsClassifier = dictDescriptionParamsClassifier;

        this.nameClassifier = nameClassifier;

        // size of canvas to psh on center
        this.sizeCanvas = sizeCanvas;

        // variable can toggle to know if user click the shape or move the shape.
        this.isStateClick = true;
        this.setup();
    }

    // extend of container to create round shape with name inside
    var p = createjs.extend(ShapeGenerator, createjs.Container);

    // setup the shape
    p.setup = function () {
        var text = new createjs.Text(this.nameClassifier.replace(/([A-Z])/g, ' $1').trim(), "20px Arial", "#000");
        text.textAlign = "center";
        text.maxWidth = 100;
        text.lineWidth = 100;
        text.y = -1 * text.getMeasuredHeight() / 2;

        var background = new createjs.Shape();

        var color = '';

        switch (this.typeOfClassifier) {
            case "classifier":
                color = "#fff700";
                break;

            case "regressor":
                color = "#ffa0af";
                break;

            default:
                color = "#00ff00";
                break;
        }

        background.graphics.beginFill(color).drawCircle(0, 0, 50);
        this.addChild(background, text);

        // define function for interaction
        this.on("click", this.handleClick);
        this.on("pressup", this.handlePressUp);
        this.on("pressmove", this.handlePressMove);

        // define the type of cursor
        this.cursor = "arrow";

        // with this shit
        this.mouseChildren = false;

        this.offset = Math.random() * 10;
        this.count = 0;

        this.x = this.sizeCanvas["width"] / 2;
        this.y = this.sizeCanvas["height"] / 2;
    };

    p.handleClick = function (event) {
        if (this.isStateClick) {
            shareRenderInitFormulaireShape();
            shareRenderFormShape(this.dicParamsClassifier, this.dictDescriptionParamsClassifier, this.nameClassifier, this.name);
        }
    };

    p.handlePressUp = function (event) {
        if (this.isStateClick == false) {
            window.hitShape(this.name);
        }
        this.isStateClick = true;

    };

    p.handlePressMove = function (event) {
        event.target.x = event.stageX;
        event.target.y = event.stageY;
        this.isStateClick = false;
    };

    // return dict containe name of classifier and dict with params of classifier
    // like this {name : {Params1:value1, Params2:value2}}
    p.getDataDict = function () {
        var temp = {};
        temp[this.nameClassifier] = this.dicParamsClassifier;
        return temp;
    };

    p.updateDictData = function (dictParamsClassifier) {
        this.dicParamsClassifier = dictParamsClassifier;
    };

    p.resetPositionShape = function () {

        this.x = this.sizeCanvas["width"] / 2;
        this.y = this.sizeCanvas["height"] / 2;
    };
    // create window function. when, i can create shape in a script on the page index.html
    window.ShapeGenerator = createjs.promote(ShapeGenerator, "Container");
}());