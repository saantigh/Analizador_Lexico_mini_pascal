program TestExpr;
begin
  if (not (5 < 3) and (10 >= 2 xor 4 div 2)) or true then
    writeln('OK')
  else
    writeln('Error');
end.
