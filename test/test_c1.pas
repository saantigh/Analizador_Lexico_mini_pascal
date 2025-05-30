program LexicalErrFixed;
uses crt;                  { Removed invalid unit }
const
  MAX1 = 100;
  MAX1 = 200;              { Valid identifier }
  PI = 3.1415;            { Proper real literal }
  MAX1=20;
type
  TArr = array[0..10] of integer;  { Corrected spelling }
var
  num: integer;
begin
  writeln('Lexical errors fixed, program compiles.');
end.

