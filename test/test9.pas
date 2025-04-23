program TestLoops;
var i: integer;
begin
  for i := 1 to 10 do
    writeln(i);
  i := 1;
  while i < 5 do
  begin
    writeln(i);
    i := i + 1;
  end;
end.
