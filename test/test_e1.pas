program LexicalErr;
uses crt,@invalid;  { '@' is an invalid character in a uses clause }
const
  1MAX = 100;       { Identifier cannot begin with a digit }
  PI = 3.14.15;     { Malformed real literal: only one dot allowed }
type
  TArr = array[0..10] of integar;  { misspelled 'integer' }
var
  num: integer;
begin
  writeln('This won''t compile due to lexical errors');
end.
