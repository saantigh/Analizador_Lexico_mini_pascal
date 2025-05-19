program SyntaxErr
const
  a: integer = 5        { Missing semicolon after header and const }
var
  b: integer;
begin
  if a > 0 then         { Missing 'begin' for compound statement }
    writeln('Positive')
  else
    writeln('Non-positive');
  for i := 1 to 10 do   { 'i' undeclared }
    writeln(i);
end                       { Missing period }

