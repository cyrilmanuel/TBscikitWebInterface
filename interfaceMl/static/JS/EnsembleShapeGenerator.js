(function () {

    // constructor shape
    function EnsembleShapeGenerator(nameOfficeID, sizeCanvas, dictClassifier1, dictClassifier2) {
        this.Container_constructor();
        // stock the name of the classifier this shape will be repr
        this.name = nameOfficeID.toString();

        this.offset = 0;

        this.idSubShapeGenerator = 0;
        // stock the params of the classifier into the shape
        // because this shape can call the function to render
        // with React, a approprieted form
        this.dicParamsClassifier = {};
        this.nameClassifier = "ensemble Learning";

        // size of canvas to psh on center
        this.sizeCanvas = sizeCanvas;

        // variable can toggle to know if user click the shape or move the shape.
        this.isStateClick = true;
        this.setup();
        this.addClassifier(dictClassifier1);
        this.addClassifier(dictClassifier2);
    }

    // extend of container to create round shape with name inside
    var p = createjs.extend(EnsembleShapeGenerator, createjs.Container);

    // setup the shape
    p.setup = function () {
        var text = new createjs.Text(this.nameClassifier, "20px Arial", "#000");
        text.maxWidth = 150;
        text.y = 0;
        this.offset = text.getMeasuredHeight() + 5;

        var background = new createjs.Shape();
        var color = '#10ffee';
        background.graphics.beginFill(color).drawRoundRect(0, 0, 150, 100, 15);
        this.addChild(background, text);

        // define function for interaction
        this.on("pressup", this.handlePressUp);
        this.on("pressmove", this.handlePressMove);
        this.on("click", this.handleClick);


        // with this shit
        this.mouseChildren = false;

        this.x = this.sizeCanvas["width"] / 2;
        this.y = this.sizeCanvas["height"] / 2;
    };


    p.handlePressUp = function () {
        this.isStateClick = true;
    };

    p.handlePressMove = function (event) {
        event.target.x = event.stageX - 75;
        event.target.y = event.stageY - 50;
        this.isStateClick = false;
    };

    p.handleClick = function (event) {
        shareRenderInitFormulaireShape();
        shareRenderEnsembleList(this.dicParamsClassifier, this.name);
    };

    p.addClassifier = function (dictClassifier) {
        let containerTemp = new createjs.Container();
        containerTemp.x = 0;
        containerTemp.y = this.offset + this.idSubShapeGenerator * 25;
        let backgroundTemp = new createjs.Shape();
        let colorTemp = '#fff700';
        backgroundTemp.graphics.beginFill(colorTemp).drawRoundRect(0, 0, 150, 20, 10);
        containerTemp.name = this.idSubShapeGenerator;
        let textTemp = new createjs.Text(Object.keys(dictClassifier)[0].replace(/([A-Z])/g, ' $1').trim(), "15px Arial", "#000");
        textTemp.maxWidth = 140;
        textTemp.y = 0;
        textTemp.x = 10;
        this.dicParamsClassifier[this.idSubShapeGenerator] = dictClassifier;
        containerTemp.addChild(backgroundTemp, textTemp);
        this.addChild(containerTemp);
        this.idSubShapeGenerator++;
    };
    // return dict containe name of classifier and dict with params of classifier
    // like this {name : {Params1:value1, Params2:value2}}
    p.getDataDict = function () {
        let temp = {};
        temp[this.nameClassifier] = this.dicParamsClassifier;
        return temp;
    };

    p.updateDictData = function (idShapeChild, dictParamsClassifier) {
        this.dicParamsClassifier[idShapeChild] = dictParamsClassifier;
    };

    p.removeSubShape = function (idShapeChild) {
        if (this.children.length <= 3) {
            window.removeShape(this.name);
        } else {
            for (let child in this.children) {
                if (this.children[child].name == idShapeChild) {
                    this.removeChild(this.children[child]);
                    delete this.dicParamsClassifier[idShapeChild];
                    shareRenderInitFormulaireShape();
                    break;
                }
            }
        }
    };


    // create window function. when, i can create shape in a script on the page index.html
    window.EnsembleShapeGenerator = createjs.promote(EnsembleShapeGenerator, "Container");
}());