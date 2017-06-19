(function() {

function SVM(c, gamma, kernel) {
	this.Container_constructor();

	this.kernel = kernel;
	this.c = c;
	this.gamma = gamma;
	this.setup();
}
var p = createjs.extend(SVM, createjs.Container);


p.getData = function () {
    return {"C":this.c};
}

p.setup = function() {
	var text = new createjs.Text("SVM", "20px Arial", "#000");
    text.y = -7;
	text.textAlign = "center";


	var background = new createjs.Shape();
	background.graphics.beginFill("#c7f4b7").drawCircle(0, 0, 50);
	this.addChild(background, text);

	this.on("click", this.handleClick);
	this.on("rollover", this.handleRollOver);
	this.on("rollout", this.handleRollOver);
	this.cursor = "pointer";

	this.mouseChildren = false;

	this.offset = Math.random()*10;
	this.count = 0;

	this.x = this.y = 50;
} ;

p.handleClick = function (event) {
	alert("You clicked on a button: SVM ");
} ;

p.handleRollOver = function(event) {
	this.alpha = event.type == "rollover" ? 0.4 : 1;
};

window.SVM = createjs.promote(SVM, "Container");
}());