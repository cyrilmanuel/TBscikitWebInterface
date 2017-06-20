(function () {

    // constructor shape
    function TrashGenerator(name, sizeCanvas) {
        this.Container_constructor();
        // stock the name of the classifier this shape will be repr
        this.name = name;
        this.sizeCanvas = sizeCanvas;
        this.setup();
    }
    // extend of container to create round shape with name inside
    var p = createjs.extend(TrashGenerator, createjs.Container);

    // setup the shape
    p.setup = function () {
        this.text = new createjs.Text(this.name, "20px Arial", "#000");
        this.text.y = -7;
        this.text.textAlign = "center";

        var background = new createjs.Shape();
        var color = '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
        background.graphics.beginFill(color).drawCircle(0, 0, 50);
        this.addChild(background, this.text);

        this.mouseChildren = false;

        this.offset = Math.random() * 10;
        this.count = 0;

        this.x = this.sizeCanvas["width"]- 50;
        this.y = this.sizeCanvas["height"] - 50;
    };
    // create window function. when, i can create shape in a script on the page index.html
    window.TrashGenerator = createjs.promote(TrashGenerator, "Container");
}());