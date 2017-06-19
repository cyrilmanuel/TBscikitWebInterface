(function () {

    function ShapeGenerator(name) {
        this.Container_constructor();
        this.name = name;
        this.dicParams = getData()[this.name];
        this.isStateClick = true;
        this.setup();
    }
    var p = createjs.extend(ShapeGenerator, createjs.Container);


    p.setup = function () {
        this.text = new createjs.Text(this.name, "20px Arial", "#000");
        this.text.y = -7;
        this.text.textAlign = "center";

        var background = new createjs.Shape();
        background.graphics.beginFill("#c7f4b7").drawCircle(0, 0, 50);
        this.addChild(background, this.text);

        this.on("click", this.handleClick);
        this.on("rollover", this.handleRollOver);
        this.on("rollout", this.handleRollOver);
        this.on("pressup", this.handlePressUp);
        this.on("pressmove", this.handlePressMove);

        this.cursor = "arrow";

        this.mouseChildren = false;

        this.offset = Math.random() * 10;
        this.count = 0;

        this.x = this.y = 50;
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

    p.getDataDict = function () {
        var temp = {};
        temp[this.name]=this.dicParams;
        return temp;
    }
    window.ShapeGenerator = createjs.promote(ShapeGenerator, "Container");
}());