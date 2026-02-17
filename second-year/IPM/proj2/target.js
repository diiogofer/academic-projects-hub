class Target {
  constructor(x, y, w, h, l, id) {
    this.x = x;
    this.y = y;
    this.width = w;
    this.height = h;
    this.label = String(l);
    this.id = id;
    this.color = this.getColorForFirstLetter();
  }

  clicked(mouse_x, mouse_y) {
    return (
      mouse_x >= this.x - this.width / 2 &&
      mouse_x <= this.x + this.width / 2 &&
      mouse_y >= this.y - this.height / 2 &&
      mouse_y <= this.y + this.height / 2
    );
  }

  getColorForFirstLetter() {
    let firstLetter = this.label.charAt(0).toUpperCase();
    let colors = {
      A: color(150, 70, 60),
      B: color(50, 120, 200),
      C: color(190, 100, 80),
      D: color(70, 140, 100),
      E: color(160, 90, 130),
      F: color(210, 170, 90),
      G: color(90, 160, 140),
      H: color(180, 110, 180),
      I: color(200, 130, 80),
      J: color(100, 180, 110),
      K: color(130, 100, 180),
      L: color(210, 140, 110),
      M: color(90, 140, 200),
      N: color(190, 120, 110),
      O: color(80, 170, 190),
      P: color(190, 80, 140),
      Q: color(120, 190, 120),
      R: color(180, 90, 110),
      S: color(100, 130, 200),
      T: color(160, 170, 90),
      U: color(130, 170, 180),
      V: color(180, 110, 160),
      W: color(80, 190, 120),
      X: color(140, 140, 190),
      Y: color(190, 160, 100),
      Z: color(120, 120, 120)
    };

    return colors[firstLetter] || color(200);
  }

draw() {
  push();

  fill(this.color);
  stroke(0);
  strokeWeight(2);
  rectMode(CENTER);
  rect(this.x, this.y, this.width, this.height, 12);

  if (this.label.length > 0) {
    let fullText = this.label;
    let firstLetter = fullText.charAt(0);

    textAlign(CENTER, CENTER);

    let firstLetterSize = this.height * 0.45;
    textFont("Arial", firstLetterSize);
    textStyle(BOLD);
    stroke(0);
    strokeWeight(6);
    fill(255);
    text(firstLetter, this.x, this.y - this.height * 0.2);

    textStyle(NORMAL);
    fill(255);
    strokeWeight(3);

    let baseSize = this.height * 0.2;
    textFont("Arial", baseSize);

    const forceOneLine = ["George Town", "Ribeirao Preto"];

    if (
      fullText.includes(" ") &&
      textWidth(fullText) > this.width * 0.9 &&
      !forceOneLine.includes(fullText)
    ) {
      let splitIndex = fullText.lastIndexOf(" ", fullText.length / 2);
      let line1 = fullText.substring(0, splitIndex).trim();
      let line2 = fullText.substring(splitIndex).trim();

      let smallerSize = baseSize * 0.95;
      textFont("Arial", smallerSize);

      let lineHeight = textAscent() + textDescent();
      let centerY = this.y + this.height * 0.25;

      text(line1, this.x, centerY - lineHeight / 2);
      text(line2, this.x, centerY + lineHeight / 2);
    } else {
      if (textWidth(fullText) > this.width * 0.9) {
        let scaledSize = baseSize * (this.width * 0.9 / textWidth(fullText));
        textFont("Arial", scaledSize);
      }

      let centerY = this.y + this.height * 0.22;
      text(fullText, this.x, centerY);
    }
  }

  pop();
}

}
