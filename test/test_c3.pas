program SemanticErrFixed;
var
  x: integer;
  s: string;
begin
  x := 10;               { Proper integer assignment }
  writeln(x);            { 'x' is declared }
  s := 'Value: ' + IntToStr(x); { Convert integer to string }
end.
