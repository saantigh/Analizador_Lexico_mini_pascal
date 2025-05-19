program SyntaxErrFixed;   { Added semicolon }
const
  a: integer = 5;         { Added semicolon }
var
  b, i: integer;          { Declared i }
begin
  if a > 0 then           { Single statement is okay without 'begin' }
    writeln('Positive')
  else
    writeln('Non-positive');
  for i := 1 to 10 do     { Now 'i' exists }
    writeln(i);
end.                      { Added period }

