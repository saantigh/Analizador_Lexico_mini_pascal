program TestComplex;
uses crt;
const
  MAX = 100;
type
  TRec = record
    x: integer;
    y: real;
  end;
var
  arr: ARRAY[1..MAX] of TRec;
  ptr: ^TRec;

function Sum(a, b: integer): integer;
begin
  Sum := a + b;
end;

procedure DoSomething;
begin
  ptr^.x := 0;
end;

begin
  writeln('Hello World');
end.
