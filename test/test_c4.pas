program StressTestFixed;
uses crt;
const
  A = 10;
  B = 20;
type
  TInt = integer;
  TGood = record             { Define a proper record }
    v: integer;
  end;
var
  x, y: integer;             { Both declared and comma-separated }
begin
  x := A + B;                { Use '+' instead of '**' }
  y := A * B;                { Another valid operation }
  writeln('Sum=', x + y);    { Added semicolon }
end.

