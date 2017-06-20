(function () {

    // constructor shape
    function ShapeGenerator(name, sizeCanvas) {
        this.Container_constructor();
        // stock the name of the classifier this shape will be repr
        this.name = name;
        // stock the params of the classifier into the shape
        // because this shape can call the function to render
        // with React, a approprieted form
        this.dicParams = getData()[this.name];

        this.sizeCanvas = sizeCanvas;
        // variable can toggle to know if user click the shape or move the shape.
        this.isStateClick = true;
        this.setup();
    }
    // extend of container to create round shape with name inside
    var p = createjs.extend(ShapeGenerator, createjs.Container);

    // setup the shape
    p.setup = function () {
        this.text = new createjs.Text(this.name, "20px Arial", "#000");
        this.text.y = -7;
        this.text.textAlign = "center";

        var background = new createjs.Shape();
        var color = '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
        background.graphics.beginFill(color).drawCircle(0, 0, 50);
        this.addChild(background, this.text);

        // define function for interaction
        this.on("click", this.handleClick);
        this.on("rollover", this.handleRollOver);
        this.on("rollout", this.handleRollOver);
        this.on("pressup", this.handlePressUp);
        this.on("pressmove", this.handlePressMove);

        // define the type of cursor
        this.cursor = "arrow";

        this.mouseChildren = false;

        this.offset = Math.random() * 10;
        this.count = 0;

        this.x = this.sizeCanvas["width"] / 2;
        this.y = this.sizeCanvas["height"] / 2;
    };

    p.handleClick = function (event) {
        if (this.isStateClick) {
         shareRenderFormShape(this.dicParams);
        }
    };

    p.handleRollOver = function (event) {
        this.alpha = event.type == "rollover" ? 0.4 : 1;
    };

    p.handlePressUp = function (event) {
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
        temp[this.name]=this.dicParams;
        return temp;
    }
    // create window function. when, i can create shape in a script on the page index.html
    window.ShapeGenerator = createjs.promote(ShapeGenerator, "Container");
}());