(*Hola soy 
iavn*)

//Otro commmentario aaa

var nombre@a := 10;

256yanda;;;;;;
program EjemploCompleto;  { Nombre del programa }
uses crt;  { Librería para funciones de pantalla }

const
  PI = 3.1416;
  MENSAJE = '¡Hola, Pascal!';

type
  TNumero = real;
  TEntero = integer;

var
  a, b, c: TEntero;    { Variables enteras }
  x, y: TNumero;       { Variables reales }
  i: InTeger;
  arreglo: array[1..5] of integer;
  puntero: ^integer;
  nombre_usuario: string;
  es_valido: boolean;

begin
  clrscr;  { Limpia la pantalla }

  { Asignaciones }
  a := 10; 
  b := -5; 
  c := a + b * 2; { Operaciones matemáticas con símbolos +, -, * }
  
  x := 2.5;
  y := -12.12;
  
  { Comparaciones }
  if (x > y) and (c <> b) then
    writeln('x es mayor que y y c es diferente de b');

  { Bucle for con range .. }
  for i := 1 to 5 do
    arreglo[i] := i * 2;

  { Bucle while }
  i := 1;
  while i <= 5 do
  begin
    writeln('Arreglo[', i, '] = ', arreglo[i]);
    i := i + 1;
  end;

  { Case con rango .. }
  case a of
    1..5: writeln('El valor de a está entre 1 y 5');
    6, 7, 8: writeln('El valor de a es 6, 7 o 8');
    else writeln('El valor de a no está en los rangos definidos');
  end;

  { Uso de punteros }
  new(puntero);  
  puntero^ := 100;
  writeln('Valor del puntero: ', puntero^);
  dispose(puntero);

  { Operaciones con booleanos }
  es_valido := true;
  if not es_valido then
    writeln('No es válido')
  else
    writeln('Es válido');

  { Entrada y salida }
  write('Ingrese su nombre: ');
  readln(nombre_usuario);
  writeln('Bienvenido, ', nombre_usuario);

  { Fin del programa }
  writeln(MENSAJE);
  writeln('Presione una tecla para salir...');
  readkey;  { Espera una tecla }
end.

'a