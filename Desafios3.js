function imc (altura,peso){
    let imc = peso / (altura * altura);
    return imc;
}
imc(70,1.75);

function factorial(n){
    let factorial = 1;
    for (let i = 1; i <= n; i++){
        factorial *=i;
    }
    return factorial;
}

factorial(3);

function dolares(d){
    let cambio = 4.80;
    let reales = d * cambio;
    return reales;
}

dolares(2);

function area(altura,anchura){
    let a = altura;
    let an = anchura;
    let re = a * an;
    return re;
}
area(4,6)

function sala(radio1){
    const pi = 3.14;
    let area = pi * radio1 * radio1;
    return area;
}
sala(4.3)

function tablaM(numer){
    let tabla = 1;
    for( i = 1; i <= 10; i++){
        tabla += `${numer} x ${i} = ${numer * i}<br>`;
    }  
}

tablaM(3);