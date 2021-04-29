const ruleta = document.querySelector("#ruleta");

ruleta.addEventListener("click", girar);

randAnterior = 0
signo = 1

function girar() {
  signo = signo * -1
  calcular(signo, 0.9);
}

function asignarContrato(c) {
  document.querySelector("#contrato").innerHTML = "Contrato: " + c;
}


function calcular(signo, probA) {
  // 0: contrato A, 1:contrato B
  let contrato = Math.random()
  var giro = 0
  if (contrato <= probA) {
    giro = 360 * 5
  } else {
    giro = 360 * 5 + 180
  }
  ruleta.style.transform = "rotate(" + giro * signo + "deg)";
  setTimeout(() => {
    if (contrato <= probA) {
      asignarContrato("A");
    } else {
      asignarContrato("B");
    }
  }, 5000);
}