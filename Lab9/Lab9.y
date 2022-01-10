%{
        #include <stdio.h>
        #include <stdlib.h>
        #include <string.h>
        #define YYDEBUG 1

        int yylex();
        void yyerror();

        int production_string[100];
        int production_string_length = 0;

        void addToProductionString(int production_number) {
                production_string[production_string_length++] = production_number;
        }

        void printProductionString() {
                int index;
                for(index = 0; index < production_string_length; index++){
                        printf("%d", production_string[index]);
                }
                printf("/n");
        }
%}

%token SUM
%token SUBTRACT
%token MULTIPLY
%token DIVIDE
%token LOWER
%token GREATER
%token ASSIGN
%token DEFINE
%token EQUAL
%token LOWEREQUAL
%token GREATEREQUAL
%token NOTEQUAL
%token AND
%token OR
%token IN
%token OUT

%token IF
%token ELSE
%token INT
%token CHAR
%token WHILE

%token TWODOTS
%token DOTCOMMA
%token OPENSQUARE
%token CLOSESQUARE
%token OPENBRACKET
%token CLOSEBRACKET

%token ID

%token CONST_CHAR
%token CONST_STRING
%token CONST_NUMBER

%left SUM SUBTRACT
%left MULTIPLY DIVIDE
%left OR
%left AND

%%
relation:   LOWER {addToProductionString(1);}
        |   LOWEREQUAL  {addToProductionString(2);}
        |   EQUAL       {addToProductionString(3);}
        |   NOTEQUAL    {addToProductionString(4);}
        |   GREATEREQUAL        {addToProductionString(5);}
        |   GREATER         {addToProductionString(6);}
        ;

logical_operator:   OR          {addToProductionString(7);}
                |   AND         {addToProductionString(8);}
                ;

program:    OPENBRACKET stmt CLOSEBRACKET        {addToProductionString(9);}
        ;

stmt:   
        |   simple_stmt         {addToProductionString(10);}
        |   struct_stmt stmt    {addToProductionString(11);}
        ;

simple_stmt:    declaration_stmt DOTCOMMA    {addToProductionString(12);}
                |   assignment_stmt DOTCOMMA {addToProductionString(13);}
                |   io_stmt DOTCOMMA         {addToProductionString(14);}
                ;

declaration_stmt:   DEFINE ID TWODOTS type     {addToProductionString(15);}
                ;

type:   generic_type            {addToProductionString(16);}
        |   array_declaration   {addToProductionString(17);}
        ;

generic_type:   CHAR            {addToProductionString(18);}
                |   INT         {addToProductionString(19);}
                ;

array_declaration:  generic_type OPENSQUARE CONST_NUMBER CLOSESQUARE   {addToProductionString(20);}
                ;

assignment_stmt:    ID ASSIGN expression   {addToProductionString(21);}
                ;

expression:     expression_sign expression_sequence     {addToProductionString(22);}
                ;

expression_sequence:    expression_sign         {addToProductionString(23);}
                        |   ID                  {addToProductionString(24);}
                        |   CONST_NUMBER        {addToProductionString(25);}
                        |   expression_sign  expression_sequence        {addToProductionString(26);}
                        |   ID expression_sequence                      {addToProductionString(27);}
                        |   CONST_NUMBER expression_sequence            {addToProductionString(28);}
                        ;

expression_sign:    SUM         {addToProductionString(29);}
                |   SUBTRACT         {addToProductionString(30);}
                |   MULTIPLY         {addToProductionString(31);}
                |   DIVIDE         {addToProductionString(32);}
                ;

in_out:     IN          {addToProductionString(33);}
        |   OUT         {addToProductionString(34);}        
        ;

io_stmt:    in_out ID   {addToProductionString(35);}
        |   in_out CONST_STRING         {addToProductionString(36);}
        |   in_out CONST_CHAR           {addToProductionString(37);}
        ;

struct_stmt:    if_stmt         {addToProductionString(38);}
                |   while_stmt  {addToProductionString(39);}
                ;

if_stmt:    IF condition OPENBRACKET stmt CLOSEBRACKET   {addToProductionString(40);}
        |   IF condition OPENBRACKET stmt CLOSEBRACKET ELSE OPENBRACKET stmt CLOSEBRACKET         {addToProductionString(41);}
        ;

while_stmt:     WHILE condition OPENBRACKET stmt CLOSEBRACKET    {addToProductionString(42);}
                ;

condition:  expression relation expression      {addToProductionString(43);}
        |   expression relation expression logical_operator condition   {addToProductionString(44);}
        ;
%%

void yyerror(char *s){
        printf("%s\n", s);
}

extern FILE *yyin;

int main(int argc, char **argv){
        if(argc>1) yyin = fopen(argv[1], "r");
        if((argc>2)&&(!strcmp(argv[2],"-d"))) yydebug = 1;
        if(!yyparse()) printProductionString();
}       


