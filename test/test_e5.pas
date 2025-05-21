program TestSemantico1;
var
  a: integer;
  b: real;
begin
  a := 3.14;       { ERROR: asignación de real a entero }
  writeln(a);
end.

