program DynamicArrays;
type
  TIntArray = array of integer;
var
  arr: TIntArray;
  i: integer;
  
begin
  SetLength(arr, 10);
  
  for i := 0 to 9 do
    arr[i] := i * i;
    
  for i := 0 to High(arr) do
    writeln(arr[i]);
    
  SetLength(arr, 5);  // Shrink array
  
  writeln('After resizing:');
  for i := 0 to High(arr) do
    writeln(arr[i]);
end.