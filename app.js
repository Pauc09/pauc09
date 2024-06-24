//Se estan conectado el HTML con Js por medio del 'DOCUMENT' esto forma un puente.
//Con el 'querySelector' puedo agregarle atributos a un objecto.

/*let titulo = document.querySelector('h1');
titulo.innerHTML = "Juego del número secreto";*/

let numSecret = 0;
let nIntentos = 0;
let listaNumeros = [];
let numeroMaximo = 10;

console.log(numSecret);

function asignarTexto(elemento,texto){
    let elementoHTMl = document.querySelector(elemento);
    elementoHTMl.innerHTML = texto;
    return;
}

function vIntento(){
    let nUsuario =parseInt(document.getElementById('valorUsuario').value);

    if (nUsuario === numSecret){
        asignarTexto('p', `¡ Acertaste el número! =) en ${nIntentos} ${(nIntentos === 1) ? `intento` : 'intentos'}`);
        document.getElementById('reiniciar').removeAttribute('disabled');
    } else {
    if (nUsuario > numSecret){
        asignarTexto('p', 'El número secreto es menor');
    } else {
        asignarTexto('p','El número secreto es mayor');
        } nIntentos++;
        limpiar();
    } return;

}

function limpiar(){
    document.querySelector('#valorUsuario').value = '';
}

function nSecret() {
    let numeroGenerado = Math.floor(Math.random()*numeroMaximo)+1;
    console.log(numeroGenerado);
    console.log(listaNumeros);
    if(listaNumeros.length == numeroMaximo){
        asignarTexto('p','Ya se sortearon todos los números posibles')
    }
    else {
        if (listaNumeros.includes(numeroGenerado)){
            return nSecret();
        } else {
            listaNumeros.push(numeroGenerado);
            return numeroGenerado;
        }
    }
}


function condicionesIniciales(){
    asignarTexto('h1','Juego del número secreto.');
    asignarTexto('p',`Indica un número del 1 al ${numeroMaximo}`);
    numSecret = nSecret();
    nIntentos = 1;
}

function reiniciarJuego(){
    //Limpiar caja 
    limpiar();
    //Mensaje de inicio
    //Generar el numero aleatorio
    //Deshabilitar el número de intentos
    condicionesIniciales();
    //Deshabilitar el botón
    document.querySelector('#reiniciar').setAttribute('disabled','true');
}

condicionesIniciales();
