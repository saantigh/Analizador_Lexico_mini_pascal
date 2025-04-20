PROGRAM TestCompleto;

USES
  System, Math, Graphics;

CONST
  PI = 3.14159;
  VERSION = '1.0';
  MAX_SIZE = 100;
  IS_DEBUG = TRUE;
  NULL_CHAR = #0;

TYPE
  TDia = (Lunes, Martes, Miercoles, Jueves, Viernes, Sabado, Domingo);
  TRango = 1..100;
  TMatriz = ARRAY[1..10, 1..10] OF INTEGER;
  TVector = ARRAY[1..50] OF REAL;
  TArchivo = FILE OF INTEGER;
  TConjunto = SET OF CHAR;
  TPuntero = ^INTEGER;
  
  TRegistro = RECORD
    id: INTEGER;
    nombre: STRING[50];
    activo: BOOLEAN;
    CASE tipo: BYTE OF
      1: (valor_entero: INTEGER);
      2: (valor_real: REAL);
      3: (valor_texto: STRING[100]);
  END;
  
  TEmpleado = RECORD
    codigo: INTEGER;
    nombre: STRING[50];
    salario: REAL;
    departamento: STRING[30];
  END;
  
  TListaEmpleados = ARRAY[1..50] OF TEmpleado;
  
  TPunto = OBJECT
    x, y: REAL;
    CONSTRUCTOR Inicializar(coord_x, coord_y: REAL);
    PROCEDURE Mover(dx, dy: REAL);
    FUNCTION Distancia(otro: TPunto): REAL;
    DESTRUCTOR Liberar;
  END;

VAR
  i, j, k, suma, contador: INTEGER;
  x, y, z, promedio: REAL;
  nombre, apellido, texto: STRING[50];
  bandera, condicion: BOOLEAN;
  dias: TDia;
  matriz: TMatriz;
  vector: TVector;
  registro: TRegistro;
  empleados: TListaEmpleados;
  arch: TArchivo;
  conj: TConjunto;
  ptr: TPuntero;
  punto: TPunto;

PROCEDURE ImprimirMensaje(mensaje: STRING); FORWARD;

FUNCTION CalcularArea(base, altura: REAL): REAL;
VAR
  resultado: REAL;
BEGIN
  resultado := base * altura / 2;
  CalcularArea := resultado;
END;

FUNCTION Factorial(n: INTEGER): INTEGER;
BEGIN
  IF n <= 1 THEN
    Factorial := 1
  ELSE
    Factorial := n * Factorial(n - 1);
END;

PROCEDURE ProcesarDatos(VAR datos: TMatriz; n: INTEGER);
VAR
  i, j: INTEGER;
  temp: REAL;
BEGIN
  FOR i := 1 TO n DO
  BEGIN
    FOR j := 1 TO n DO
    BEGIN
      datos[i,j] := i * j;
    END;
  END;
END;

PROCEDURE ImprimirMensaje(mensaje: STRING);
BEGIN
  { Este procedimiento imprime un mensaje en pantalla }
  writeln(mensaje);
END;

FUNCTION BuscarElemento(arreglo: TVector; tamano: INTEGER; elemento: REAL): INTEGER;
VAR
  i: INTEGER;
  encontrado: BOOLEAN;
BEGIN
  encontrado := FALSE;
  i := 1;
  WHILE (i <= tamano) AND (NOT encontrado) DO
  BEGIN
    IF arreglo[i] = elemento THEN
      encontrado := TRUE
    ELSE
      i := i + 1;
  END;
  
  IF encontrado THEN
    BuscarElemento := i
  ELSE
    BuscarElemento := 0;
END;

PROCEDURE OrdenarBurbuja(VAR arr: TVector; n: INTEGER);
VAR
  i, j: INTEGER;
  temp: REAL;
BEGIN
  FOR i := 1 TO n-1 DO
    FOR j := 1 TO n-i DO
      IF arr[j] > arr[j+1] THEN
      BEGIN
        temp := arr[j];
        arr[j] := arr[j+1];
        arr[j+1] := temp;
      END;
END;

PROCEDURE ManejarCasos(opcion: INTEGER);
BEGIN
  CASE opcion OF
    1: ImprimirMensaje('Opción 1 seleccionada');
    2: ImprimirMensaje('Opción 2 seleccionada');
    3, 4: ImprimirMensaje('Opción 3 o 4 seleccionada');
    5..10: ImprimirMensaje('Opción entre 5 y 10 seleccionada');
  ELSE
    ImprimirMensaje('Opción no válida');
  END;
END;

PROCEDURE EjemploWith;
VAR
  emp: TEmpleado;
BEGIN
  WITH emp DO
  BEGIN
    codigo := 1001;
    nombre := 'Juan Pérez';
    salario := 2500.50;
    departamento := 'Sistemas';
  END;
END;

PROCEDURE RecorrerConjunto(conj: TConjunto);
VAR
  c: CHAR;
BEGIN
  FOR c := 'A' TO 'Z' DO
    IF c IN conj THEN
      writeln(c, ' está en el conjunto');
END;

FUNCTION Max(a, b: INTEGER): INTEGER;
BEGIN
  IF a > b THEN
    Max := a
  ELSE
    Max := b;
END;

PROCEDURE ProcedimientoAnidado;
VAR
  x: INTEGER;

  PROCEDURE Interno;
  VAR
    y: INTEGER;
  BEGIN
    y := x + 5;
    writeln(y);
  END;

BEGIN
  x := 10;
  Interno;
END;

CONSTRUCTOR TPunto.Inicializar(coord_x, coord_y: REAL);
BEGIN
  x := coord_x;
  y := coord_y;
END;

PROCEDURE TPunto.Mover(dx, dy: REAL);
BEGIN
  x := x + dx;
  y := y + dy;
END;

FUNCTION TPunto.Distancia(otro: TPunto): REAL;
VAR
  dx, dy: REAL;
BEGIN
  dx := x - otro.x;
  dy := y - otro.y;
  Distancia := SQRT(dx*dx + dy*dy);
END;

DESTRUCTOR TPunto.Liberar;
BEGIN
  { Limpieza del objeto }
END;

PROCEDURE TestRepeatUntil;
VAR
  i: INTEGER;
BEGIN
  i := 1;
  REPEAT
    writeln('Iteración: ', i);
    i := i + 1;
  UNTIL i > 10;
END;

PROCEDURE TestEtiquetas;
LABEL 100, 200;
BEGIN
  GOTO 100;
  writeln('Esto no se ejecuta');
  
  100:
  writeln('Salto a etiqueta 100');
  IF i > 10 THEN
    GOTO 200;
  
  writeln('Continuando ejecución');
  
  200:
  writeln('Fin del procedimiento');
END;

BEGIN
  { Programa principal }
  writeln('Iniciando programa de prueba completo');
  
  { Inicialización de variables }
  i := 1;
  x := 3.14;
  nombre := 'Pascal';
  bandera := TRUE;
  
  { Operaciones aritméticas }
  suma := 5 + 3 * 2;
  x := (y + z) * 2.5;
  promedio := (x + y + z) / 3;
  
  { Operaciones lógicas }
  condicion := (i > 0) AND (j < 10) OR NOT bandera;
  
  { Asignación de conjunto }
  conj := ['A'..'Z', 'a'..'z', '0'..'9'];
  
  { Asignación de puntero }
  New(ptr);
  ptr^ := 42;
  
  { Instrucción IF-THEN-ELSE }
  IF x > 10 THEN
  BEGIN
    writeln('x es mayor que 10');
    x := x - 10;
  END
  ELSE
  BEGIN
    writeln('x no es mayor que 10');
    x := x + 10;
  END;
  
  { Instrucción CASE }
  CASE i OF
    1: writeln('Uno');
    2: writeln('Dos');
    3, 4, 5: writeln('Entre tres y cinco');
    10..20: writeln('Entre diez y veinte');
  ELSE
    writeln('Otro valor');
  END;
  
  { Bucle FOR }
  FOR i := 1 TO 10 DO
  BEGIN
    writeln('Iteración ', i);
    suma := suma + i;
  END;
  
  { Bucle FOR-DOWNTO }
  FOR i := 10 DOWNTO 1 DO
    writeln('Cuenta regresiva: ', i);
  
  { Bucle WHILE }
  i := 1;
  WHILE i <= 5 DO
  BEGIN
    writeln('Ciclo while: ', i);
    i := i + 1;
  END;
  
  { Bucle REPEAT-UNTIL }
  i := 1;
  REPEAT
    writeln('Ciclo repeat: ', i);
    i := i + 1;
  UNTIL i > 5;
  
  { Llamada a procedimientos y funciones }
  ImprimirMensaje('Hola desde el programa principal');
  ProcesarDatos(matriz, 10);
  area := CalcularArea(5.0, 3.0);
  fact := Factorial(5);
  
  { Uso de WITH }
  WITH registro DO
  BEGIN
    id := 1;
    nombre := 'Registro de prueba';
    activo := TRUE;
    tipo := 1;
    valor_entero := 100;
  END;
  
  { Creación y uso de objeto }
  punto.Inicializar(10, 20);
  punto.Mover(5, -3);
  distancia := punto.Distancia(punto2);
  
  { Operaciones con archivos }
  Assign(arch, 'datos.dat');
  Reset(arch);
  WHILE NOT EOF(arch) DO
  BEGIN
    Read(arch, i);
    writeln(i);
  END;
  Close(arch);
  
  writeln('Programa de prueba finalizado');
END.
