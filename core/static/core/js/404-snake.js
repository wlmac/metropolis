let snakeC = [];
let snakeR = [];
let fruitR = 0;
let fruitC = 0;
let context = null;
let cellSide = 10;
let rows = 20;
let cols = 20;
let dir = "right";
let fps = 5;
let alive = true;
let won = false;

window.onload = function () {
    const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
    if (vw < 400) {
        cellSide = 7;
    }
    $(".display-metropolis").click(function () {
        $(this).fadeOut(100)
        $(".result-display").stop().hide();
        let canvas = $("#game-canvas")[0];
        $(canvas).attr("width", "" + (cellSide * cols));
        $(canvas).attr("height", "" + (cellSide * rows));

        $("#up-button").css("width", "" + (cellSide * cols))
        $("#down-button").css("width", "" + (cellSide * cols))
        $("#left-button").css("height", "" + (cellSide * rows))
        $("#right-button").css("height", "" + (cellSide * rows))

        $(".game-container").stop().fadeIn(300, function () {
            context = canvas.getContext("2d");
            $(".result-display-message").text("Start Game?");
            $(".result-display").click(restart);
            restart();
            $(document).keydown(function (e) {
                if ((e.key === 'w' || e.key === 'ArrowUp') && !crashes(-1, 0)) dir = "up";
                else if ((e.key === 'a' || e.key === 'ArrowLeft') && !crashes(0, -1)) dir = "left";
                else if ((e.key === 's' || e.key === 'ArrowDown') && !crashes(1, 0)) dir = 'down';
                else if ((e.key === 'd' || e.key === 'ArrowRight') && !crashes(0, 1)) dir = 'right';
            })
            $("#up-button").click(function () {
                if (!crashes(-1, 0)) {
                    dir = "up"
                }
            })
            $("#left-button").click(function () {
                if (!crashes(0, -1)) {
                    dir = "left"
                }
            })
            $("#right-button").click(function () {
                if (!crashes(0, 1)) {
                    dir = "right"
                }
            })
            $("#down-button").click(function () {
                if (!crashes(1, 0)) {
                    dir = "down"
                }
            })
        })
    })
}

function crashes(rDiff, cDiff) {
    let length = snakeR.length;
    let headR = snakeR[length - 1];
    let headC = snakeC[length - 1];
    headR += rDiff;
    headC += cDiff;
    return length > 1 && snakeR[length - 2] === headR && snakeC[length - 2] === headC;
}

function reset() {
    fruitR = 0;
    fruitC = 0;
    snakeR = [0];
    snakeC = [0];
    dir = "right";
    alive = true;
    won = false;
    $(".result-display").stop().fadeOut()
}

function restart() {
    reset();
    nextFrame();
}

function nextFrame() {
    moveSnake();
    render();
    if (alive && !won) {
        setTimeout(nextFrame, 1000 / fps);
    } else if (won) {
        $(".result-display-message").html("You Won!<br>Start Again?");
        $(".result-display").stop().fadeIn();
    } else if (!alive) {
        $(".result-display-message").html("Oops...<br>Start Again?");
        $(".result-display").stop().fadeIn();
    }
}

function inBounds(r, c, rows, cols) {
    return 0 <= r && r < rows && 0 <= c && c < cols;
}

function touchingSnake(r, c) {
    for (let i = 0; i < snakeR.length; i++) {
        if (snakeR[i] === r && snakeC[i] === c) {
            return true;
        }
    }
    return false;
}

function onFruit(r, c) {
    return fruitR === r && fruitC === c;
}

function newFruit() {
    if (snakeR.length === rows * cols) {
        won = true;
    } else {
        while (touchingSnake(fruitR, fruitC)) {
            fruitR = Math.trunc(Math.random() * rows);
            fruitC = Math.trunc(Math.random() * cols);
        }
    }
}

function moveSnake() {
    let length = snakeR.length;
    let headR = snakeR[length - 1];
    let headC = snakeC[length - 1];

    if (dir === "right") headC++;
    else if (dir === "left") headC--;
    else if (dir === "down") headR++;
    else if (dir === "up") headR--;

    if (!inBounds(headR, headC, rows, cols) || touchingSnake(headR, headC)) {
        alive = false;
    } else {
        snakeR.push(headR);
        snakeC.push(headC);
        if (onFruit(headR, headC)) {
            newFruit();
        } else {
            snakeR.shift();
            snakeC.shift();
        }
    }
}

function render() {
    let grid = []
    for (let i = 0; i < rows; i++) {
        grid.push(new Array(cols));
        grid[i].fill("black");
    }
    grid[fruitR][fruitC] = "red";
    for (let i = 0; i < snakeR.length; i++) {
        if (0 <= snakeR[i] && snakeR[i] < rows && 0 <= snakeC[i] && snakeC[i] < cols) {
            grid[snakeR[i]][snakeC[i]] = "white";
        }
    }

    for (let i = 0; i < rows; i++) {
        for (let c = 0; c < cols; c++) {
            context.fillStyle = grid[i][c];
            context.fillRect(cellSide * c, cellSide * i, cellSide, cellSide);
        }
    }
}