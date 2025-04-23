program BrutalPascalDemo;
uses CRT, SysUtils;

type
  { 1) Variant record }
  TVariantRec = record
    case tag: Integer of
      0: (i: Integer);
      1: (s: String);
  end;

  { 2) Simple record }
  TPoint = record
    x, y: Integer;
  end;

  { 3) Dynamic array of records }
  TDynamicArray = array of TPoint;

  { 4) Pointer to record }
  PPoint = ^TPoint;

  { 5) Set with a numeric range }
  TIntSet = set of 1..10;

  { 6) Object‐style type with methods and dynamic array }
  TShapeObject = object
    coords: TDynamicArray;
    constructor Init(n: Integer);
    procedure Add(const pt: TPoint);
    function  Count: Integer;
  end;

var
  vr   : TVariantRec;
  arr  : TDynamicArray;
  pp   : PPoint;
  st   : TIntSet;
  shp  : TShapeObject;
  f    : file of Char;
  i    : Integer;
  tmp  : TPoint;
  txt  : String;

{--- Implementación de métodos de TShapeObject ---}
constructor TShapeObject.Init(n: Integer);
begin
  SetLength(coords, n);
end;

procedure TShapeObject.Add(const pt: TPoint);
begin
  coords[High(coords)] := pt;
end;

function TShapeObject.Count: Integer;
begin
  Count := Length(coords);
end;

begin
  ClrScr;
  {---- Variant record ----}
  vr.tag := 1;
  vr.s := '¡Pascal Brutal!';
  WriteLn('Variant string: ', vr.s);

  {---- Dynamic array + object methods ----}
  shp.Init(5);
  for i := 0 to High(shp.coords) do
    shp.Add(TPoint.Create(i, i*i));
  WriteLn('Shape has ', shp.Count, ' points');

  {---- Pointer usage ----}
  New(pp);
  pp^.x := 10; pp^.y := 20;
  WriteLn(Format('Point via pointer: (%d,%d)', [pp^.x, pp^.y]));
  Dispose(pp);

  {---- Set with range and iteration ----}
  st := [1, 3, 5..7, 10];
  Write('Set contains: ');
  for i in st do Write(i, ' ');
  WriteLn;

  {---- File of Char ----}
  Assign(f, 'demo.txt'); Rewrite(f);
  WriteLn(f, '¡Demo brutal en Pascal!');
  Close(f);
  WriteLn('File written: demo.txt');

  {---- SysUtils usage, High and Length ----}
  WriteLn('Dynamic array length is ', Length(shp.coords));
  WriteLn('High index is ', High(shp.coords));

  {---- Final message ----}
  WriteLn('¡Todo brutalmente aceptado!');
  ReadLn;
end.
