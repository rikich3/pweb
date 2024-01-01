#!/usr/bin/perl
use strinct;
use warnings;
use CGI;

sub advance{
    my $target = @_; #expresion to calculate
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
            else if($nextChar eq '+'){return $sofar + advance(substring($innerTar, 1));}
            else {return $sofar - advance(substring($innerTar, 1));}
        }
        else if($nextChar =~ /^[0-9]$/){
            my $numberStr = $1;
            $index = $index + length($numberStr);
            my $number = int($numberStr);
            if($nextInv){$sofar = $sofar / $number;}
            else {$sofar = $sofar * $number;}
            $signSafe = 0;
            $nextInv = 0;
        }
        else if($nextChar eq '*'){$index++;}
        else if($nextChar eq "/"){
            $nextInv = 1;
            $index++;
        }
        else if($nextChar eq '('){
            if ($innerTar =~ /\((.*?)\)/) {
                my $newExp = $1;
                $index = $index + length($newExp) + 2;
                $innerTar = substr($target, $index); #check if correct later
                $count = 0;
                for my $char (split //, $newExp) {
                    if($char eq '('){$count++;} #buscamos cuantos parentesis anidados hay
                }
                if($count>0) {
                    my $closed = 0
                    for my $char (split //, $innerTar) {
                        if($char eq ')'){$closed++;} #contando los cerrados en el resto para ver si hacen pares
                    }
                    if($count>$closed){
                        for (1 ..  $count - $closed){$innerTar .= ")";}
                        if($nextInv) {return $sofar / advance($innerTar);}
                        else{return $sofar * advance($innerTar);}
                    }
                    my $expComplement = untilClosure($innerTar, $count - $closed);
                    if($nextInv)$sofar = $sofar / advance($newExp.$expComplement);
                    else {$sofar = $sofar * advance($newExp.$expComplement);}
                    $index = $index + length($expComplement);
                }
                else if($nextInv){$sofar = $sofar / $newExp;}
                else {$sofar = $sofar * $newExp;}
            }
            else if($nextInv){return $sofar / advance(substr($innerTar, 1));}
            else {return $sofar * advance(substr($innerTar, 1));}
            $nextInv = 0;
        }
        else {
            $index++;
        }
    }
    return $sofar;
}

my $cgi = CGI->new;
my $expr = $cgi->param('expr');

my $solved = advance(join('', $expr =~ /[\d+\-\/\*\(\)]/g)); #regex that filters out any character that is not a number or operators
print $cgi->header('text/html');

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
