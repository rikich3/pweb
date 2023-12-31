#!/usr/bin/perl
use strict;
use warnings;
use CGI;

sub advance{
    my ($target) = @_; #expresion to calculate
    my $span = length($target);
    my $innerExp; #substring only moving forwards
    my $sofar = 1;
    my $nextInv = 0;
    my $signSafe = 1;
    my $index = 0;
    if (!$target){#caso base
        return 0;
    }
    while($index < $span){
        my $nextChar = substr($target, $index, 1);
        my $innerTar = substr($target, $index);
        my $innerSpan;
        if($nextChar eq '+' || $nextChar eq '-'){

            if($signSafe){
                if ($innerTar =~ /([+-]+)/) {
                    my $substring = $1;
                    my $count = 0;
                    for my $char (split //, $substring) {
                        if($char eq '-'){
                            $count++;
                        }
                    }
                    if(!$count%2) {$sofar = $sofar*-1;}
                }
                $signSafe = 0;
                $index++;
            }
            elsif($nextChar eq '+'){return $sofar + advance(substr($innerTar, 1));}
            else {return $sofar - advance(substr($innerTar, 1));}
        }

        elsif($nextChar =~ /^[0-9]$/){ #si es un numero
        my $numberStr;
            if ($innerTar =~ /(\d+)/) {
                $numberStr = $1;
            }
            $index = $index + length($numberStr);
            my $number = int($numberStr);
            if($nextInv){$sofar = $sofar / $number;}
            else {$sofar = $sofar * $number;}
            $signSafe = 0;
            $nextInv = 0;
        }
        elsif($nextChar eq '*'){$index++;}
        elsif($nextChar eq "/"){
            $nextInv = 1;
            $index++;
        }
        elsif($nextChar eq '('){
            if ($innerTar =~ /\((.*?)\)/) {
                my $newExp = $1;
                $index = $index + length($newExp) + 2;
                $innerTar = substr($target, $index); #check if correct later
                my $count = 0;
                for my $char (split //, $newExp) {
                    if($char eq '('){$count++;} #buscamos cuantos parentesis anidados hay
                }
                if($count>0) {
                    my $closed = 0;
                    for my $char (split //, $innerTar) {
                        if($char eq ')'){$closed++;} #contando los cerrados en el resto para ver si hacen pares
                    }
                    if($count>$closed){
                        for (1 ..  $count - $closed){$innerTar .= ")";}
                        if($nextInv) {return $sofar / advance($innerTar);}
                        else{return $sofar * advance($innerTar);}
                    }
                    my $expComplement = untilClosure($innerTar, $count - $closed);
                    if($nextInv) {$sofar = $sofar / advance($newExp.$expComplement);}
                    else {$sofar = $sofar * advance($newExp.$expComplement);}
                    $index = $index + length($expComplement);
                }
                elsif($nextInv){$sofar = $sofar / $newExp;}
                else {$sofar = $sofar * $newExp;}
            }
            elsif($nextInv){return $sofar / advance(substr($innerTar, 1));}
            else {return $sofar * advance(substr($innerTar, 1));}
            $nextInv = 0;
        }
        else {
            $index++;
        }
    }
    return $sofar;
}

sub untilClosure {
    my ($input_string, $n) = @_;

    my $substring = "";

    my $count = 0;
    for my $char (split //, $input_string) {
        $substring .= $char;

        if ($char eq ')') {
            $count++;
            last if $count == $n;
        }
    }

    return $substring;
}


my $cgi = CGI->new;
my $expr = $cgi->param('expr');
# $expr = "30-(10*2)"; #dont forget to comment this 1, in this case fails
$expr =~ s/[^0-9+\-()*\/]//g;
my $solved = advance($expr); #regex that filters out any character that is not a number or operators
print $cgi->header('text/html');
print<<BLOCK;
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div id="calculator">
    <div id="sectionTitle">Calculadora Aritmetica</div>
    <div>
        <form action="cgi-bin/solveOperation.cgi" method="get">
        <input type="text" id="inputField" placeholder="Enter expression">
        <button type="submit" class="search-button">Buscar</button>
        </form>
    </div>
    <div id="result">Result: ${solved}</div>
    <div id="textSection">
        Esta calculadora va a descartar todos los caracteres que no sean un digito, un signo aritmetico o parentesis.
    </div>
</div>
</body>
</html>
BLOCK