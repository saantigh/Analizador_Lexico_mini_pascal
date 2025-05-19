program StressTestErr; uses crt;
const A = 10 B = 20;         { Missing semicolon between constants }
type
  TInt = integer
  TBad = rec;                { 'rec' not defined }
var
  x y: TNONE;                { TNONE undeclared; missing comma }
begin
  x := A ** B;               { '**' not a Pascal operator }
  Writeln('Sum=', x+y)       { Missing semicolon and period }
end

