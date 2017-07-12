(function () {

    // constructor shape
    function EnsembleShapeGenerator(nameOfficeID, sizeCanvas, dictClassifier1, dictClassifier2, typeOfClassifier) {
        this.Container_constructor();
        // stock the name of the classifier this shape will be repr
        this.name = nameOfficeID.toString();

        this.offset = 0;
        this.typeOfClassifier = typeOfClassifier;
        this.idSubShapeGenerator = 0;
        // stock the params of the classifier into the shape
        // because this shape can call the function to render
        // with React, a approprieted form
        this.dicParamsClassifier = {};
        this.nameClassifier = "ensemble Learning";

        this.color = "";
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

        switch (this.typeOfClassifier) {
            case "classifier":
                this.color = "#10ffee";
                break;

            case "regressor":
                this.color = "#a4ffa4";
                break;

            default:
                this.color = "#ffff00";
                break;
        }
        background.graphics.beginFill(this.color).drawRoundRect(0, 0, 150, 80, 15);
        background.name = "background";
        background.graphics.height = 50;
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
        containerTemp.y = this.offset + (this.children.length - 2) * 25;
        let backgroundTemp = new createjs.Shape();

        var colorTemp = '';

        switch (this.typeOfClassifier) {
            case "classifier":
                colorTemp = "#fff700";
                break;

            case "regressor":
                colorTemp = "#ffa0af";
                break;

            default:
                colorTemp = "#00ff00";
                break;
        }
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
        this.getChildByName("background").graphics.clear().beginFill(this.color).drawRoundRect(0, 0, 150, ((this.children.length -1) * 25), 15);
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
        var isFindChild = false;
        let childNumberIndex = 0;
        if (this.children.length <= 3) {
            window.removeShape(this.name);
        } else {
            for (let child in this.children) {
                console.log(this.children[child].name);
                console.log(idShapeChild);
                console.log(this.children.length);
                if (this.children[child].name == idShapeChild) {
                    childNumberIndex = child;
                    delete this.dicParamsClassifier[idShapeChild];
                    shareRenderInitFormulaireShape();
                    isFindChild = true;
                } else {
                    if (isFindChild == true) {
                        this.children[child].y -= 25;
                    }
                }
            }
            this.removeChild(this.children[childNumberIndex]);
            this.getChildByName("background").graphics.clear().beginFill(this.color).drawRoundRect(0, 0, 150, ((this.children.length -1) * 25), 15);
        }
    };
    // create window function. when, i can create shape in a script on the page index.html
    window.EnsembleShapeGenerator = createjs.promote(EnsembleShapeGenerator, "Container");
}());