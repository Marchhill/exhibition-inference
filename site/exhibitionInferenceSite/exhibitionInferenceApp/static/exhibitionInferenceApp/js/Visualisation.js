// import * as heatmapJs from "https://cdn.skypack.dev/heatmap.js@2.0.5";
const points = [
    [20, 10],
    [20, 20],
    [25, 25],
    [30, 25],
    [50, 76]
];
const point2 = [
    [20, 11],
    [20, 22],
    [25, 5],
    [30, 45],
    [50, 26]
];
const point3 = [
    [350, 30],
    [320, 25],
    [190, 40],
    [100, 60],
    [150, 90],
    [220, 120],
    [300, 90],
    [360, 40]
];
const point4 = [
    [10, 100],
    [100, 100]
];
const point5 = [
    [10, 150],
    [100, 150]
];
let paths = [];
class path {
    constructor(data, name) {
        this.name = name;

        this.x = [];
        this.y = [];
        for (let i = 0; i < data.length; i++) {
            this.x[i] = data[i][0];
            this.y[i] = data[i][1];
        }
    }
}
let path1 = new path(points, "bob");
let path2 = new path(point2, "boo");
let path3 = new path(point3, "boa");
let path4 = new path(point4, "bos");
let path5 = new path(point5, "bog");
paths[0] = path1;
paths[1] = path2;
paths[2] = path3;
paths[3] = path4;
paths[4] = path5;

var canvas = document.getElementById("test");
var ctx = canvas.getContext("2d");

var currentPath = 0;

///*

drawPicture();
//drawLines(paths);
drawLine();

//*/
//drawTest();

function drawPicture() {
    var img = new Image();
    img.src =
        "data:image;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQCAMAAAC3Ycb+AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAGUExURQAAAAAAAKVnuc8AAAACdFJOU/8A5bcwSgAAAAlwSFlzAAAOwwAADsMBx2+oZAAAA+RJREFUeF7t0TFyw0AMBEHy/5+2dT6VlFKESxN0hwgQ7BwnKYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMW9BjkOd7xMk5tXgtwef2hsOEGTE3nCAICErw4rxsI98z8qwYiz7wlXPLW8SZIogMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMYLECBIjSIwgMY8gI9az9XLZF676W3PAerZeLvvCVc8tRwhynyAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAxgsQIEiNIjCAx/xiET+0N7xNkxt7wPkFm7A3vm/vECEFiBIkRJEaQGEFiBIkRJEaQGEFiBIkRJEaQGEFiBEk5zx+sYlzrnzFFSQAAAABJRU5ErkJggg==";
    ctx.drawImage(img, 0, 0);
}

function drawLines(paths) {
    let x = Math.random();
    //ctx.strokeStyle = 'rgb(200,0,0)';
    let r = 1;
    let g = 1;
    let b = 1;

    for (let i = 0; i < paths.length; i++) {
        //console.log(i);
        r = Math.floor(Math.random() * 255);
        g = Math.floor(Math.random() * 255);
        b = Math.floor(Math.random() * 255);
        console.log(r);
        let style = "rgb(" + r + "," + g + "," + b + ")";
        ctx.strokeStyle = style;
        ctx.fillStyle = style;
        //console.log(r);
        ctx.beginPath();

        ctx.moveTo(paths[i].x[0], paths[i].y[0]);
        for (let j = 0; j < paths[i].x.length; j++) {
            ctx.lineTo(paths[i].x[j], paths[i].y[j]);
            ctx.fillRect(paths[i].x[j] - 2, paths[i].y[j] - 2, 5, 5);
        }
        ctx.stroke();
    }
}

function drawLine() {
    draw(paths[currentPath]);
}

document.getElementById("forwardButton").onclick = function () {
    //function IncrementPath() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPicture();
    if (currentPath == paths.length - 1) {
        currentPath = 0;
    } else {
        currentPath++;
    }
    draw(paths[currentPath]);
}
document.getElementById("backButton").onclick = function () {
    //function DecrementPath() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPicture();
    if (currentPath == 0) {
        currentPath = paths.length - 1;
    } else {
        currentPath--;
    }
    draw(paths[currentPath]);
}

function drawTest() {
    ctx.fillStyle = "rgb(200,0,0)";
    ctx.fillRect(140, 300, 50, 47); //x y size x size y
    ctx.fillStyle = "rgba(0, 0, 200)";
    ctx.fillRect(30, 30, 50, 50);
    ctx.beginPath();
    ctx.strokeStyle = "rgb(200,0,0)";
    ctx.moveTo(100, 100);
    ctx.lineTo(100, 20);
    ctx.lineTo(90, 20);
    ctx.moveTo(20, 20);
    ctx.lineTo(100, 100);
    ctx.lineTo(100, 200);
    ctx.stroke();
}

function what() {
    let x = 1;
}

function draw(line) {
    let r = 0;
    let g = 0;
    let b = 0;
    //r = Math.floor(Math.random()*255);
    //g = Math.floor(Math.random()*255);
    //b = Math.floor(Math.random()*255);
    let style = "rgb(" + r + "," + g + "," + b + ")";
    ctx.strokeStyle = style;
    ctx.fillStyle = style;
    ctx.beginPath();
    ctx.moveTo(line.x[0], line.y[0]);

    for (let j = 0; j < line.x.length; j++) {
        ctx.lineTo(line.x[j], line.y[j]);
        ctx.fillRect(line.x[j] - 2, line.y[j] - 2, 5, 5);
    }
    ctx.stroke();
}
